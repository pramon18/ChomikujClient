using CommunityToolkit.Maui.Alerts;
using CommunityToolkit.Maui.Core;
using CommunityToolkit.Maui.Storage;
using Database;
using Microsoft.Extensions.Configuration;
using Models;
using System.Collections.ObjectModel;
using System.Text;
using System.Xml.Linq;
using Util;
using static ChomikujClient.MauiProgram;

namespace ChomikujClient
{
    public partial class MainPage : ContentPage
    {
        int count = 0;

        private string path;
        private HttpClient _httpClient = new HttpClient();
        private ObservableCollection<Folder> folders = new ObservableCollection<Folder>();
        private Chomik? user = null;

        private Settings settings = MauiProgram.Services?.GetService<IConfiguration>()?.GetRequiredSection("Settings").Get<Settings>()!;

        public MainPage()
        {
            InitializeComponent();
        }

        private async Task PickFolder(CancellationToken cancellationToken)
        {
            var result = await FolderPicker.Default.PickAsync(cancellationToken);
            if (result.IsSuccessful)
            {
                path = result.Folder.Path;
                lblLocalPath.Text = path;
                await Toast.Make($"The folder was picked: Name - {result.Folder.Name}, Path - {result.Folder.Path}", ToastDuration.Long).Show(cancellationToken);
            }
            else
            {
                await Toast.Make($"The folder was not picked with error: {result.Exception.Message}").Show(cancellationToken);
            }
        }

        private async void PickFolderBtn_Clicked(object sender, EventArgs e)
        {
            await PickFolder(CancellationToken.None);
        }

        private async Task<string> SendSoapRequest(SOAPRequest request)
        {
            using (HttpClient client = new HttpClient())
            {
                foreach (var header in request.headers)
                    client.DefaultRequestHeaders.Add(header.Key, header.Value);

                HttpContent content = new StringContent(request.Content, Encoding.UTF8, "text/xml");

                HttpResponseMessage response = client.PostAsync(request.url, content).Result;

                return response.Content.ReadAsStringAsync().Result;
            }
        }

        public class SOAPRequest
        {
            public string url { get; set; }            
            public Dictionary<string, string> headers { get; set; }
            public XDocument soapEnvelope { get; set; }

            public SOAPRequest(string url, string content) 
            {
                // Headers padrão
                this.headers = new Dictionary<string, string>();
                headers.Add("User-Agent", "Mozilla/5.0");
                headers.Add("Accept-Language", "en-US,*");
                headers.Add("Accept", "*/*");

                // Envelope padrão
                this.soapEnvelope = XDocument.Parse(@"<?xml version=""1.0"" encoding=""utf-8""?>
                                                     <s:Envelope s:encodingStyle=""http://schemas.xmlsoap.org/soap/encoding/"" xmlns:s=""http://schemas.xmlsoap.org/soap/envelope/"">     
                                                        <s:Body>		                    
	                                                    </s:Body>
                                                     </s:Envelope>");
                // Destino e conteúdo
                this.url = url;
                this.Content = content;
            }

            public string _content { get; set; }
            public string Content 
            {
                get 
                {
                    return _content;
                }
                set 
                {
                    var element = XMLUtil.GetElementByName(this.soapEnvelope, "Body");
                    if (element != null) 
                    {
                        element.Add(XElement.Parse(value));
                    }

                    this._content =  this.soapEnvelope.ToString();
                }             
            }
        }

        public class Chomik
        {
            public String name { get; set; } = String.Empty;
            public String token { get; set; } = String.Empty;
            public String chomikId { get; set; } = String.Empty;
        }

        private async void LoginBtn_Clicked(object sender, EventArgs e)
        {
            // USAR URL DO CHOMIKBOX como base
            var Url = "http://box.chomikuj.pl/services/ChomikBoxService.svc";

            List<String> actions = new List<String>(){ "Auth", "Folders" };

            System.Diagnostics.Debug.WriteLine(settings.User.User, settings.User.Password);

            // Login
            var content = @$"<Auth xmlns=""http://chomikuj.pl/"">
			                    <name>{settings.User.User}</name>
			                    <passHash>{HashUtil.ComputeMD5(settings.User.Password)}</passHash>
			                    <client>
				                    <name>chomikbox</name>
				                    <version>2.0.8.2</version>
			                    </client>
                                <ver>4</ver>
                            </Auth>";

            // Montar requisição
            SOAPRequest request = new SOAPRequest(Url, content);

            request.headers.Add("SOAPAction", "http://chomikuj.pl/IChomikBoxService/Auth");

            var response = await this.SendSoapRequest(request);

            XDocument doc = XDocument.Parse(response);

            // Carregar no objeto
            this.user = new Chomik();

            var status = XMLUtil.GetValueByName(doc, "status");
            this.user.chomikId = XMLUtil.GetValueByName(doc, "hamsterId");
            this.user.name = XMLUtil.GetValueByName(doc, "name");
            this.user.token = XMLUtil.GetValueByName(doc, "token");

            this.folders = new ObservableCollection<Folder>(await this.GetFolders(this.user));

            FoldersList.ItemsSource = this.folders;

            // Criar métodos para login e buscar arquivos
            foreach(var f in this.folders)
            {
                var folder = new Folder() { Id = f.Id, Name = f.Name };
                DB.Connection.InsertOrReplaceAsync(folder).Wait();
            }
        }

        private async Task<List<Folder>> GetFolders(Chomik user, int folderId = 0)
        {
            List<Folder> result = new List<Folder>();

            // USAR URL DO CHOMIKBOX como base
            var Url = "http://box.chomikuj.pl/services/ChomikBoxService.svc";

            // NESSE PONTO DEVO TER UM USUÁRIO LOGADO
            // TENTAR PEGAR PASTAS
            var content = @$"<Folders xmlns=""http://chomikuj.pl/"">
			                    <token>{user.token}</token>
			                    <hamsterId>{user.chomikId}</hamsterId>
			                    <folderId>{folderId}</folderId>
			                    <depth>2</depth>
		                    </Folders>";

            // Depth 2 pega a primeira fileira, igual aparece no site.
            // Depth 0 pega tudo.

            SOAPRequest request = new SOAPRequest(Url, content);
            request.headers.Add("SOAPAction", "http://chomikuj.pl/IChomikBoxService/Folders");

            var response = await this.SendSoapRequest(request);

            XDocument doc = XDocument.Parse(response);

            var folders = XMLUtil.GetElementsByName(doc, "FolderInfo");

            foreach (var folder in folders)
            {
                var id = XMLUtil.GetValueByName(folder, "id");
                var name = XMLUtil.GetValueByName(folder, "name");
                Folder f = new Folder() { Id = id, Name = name };
                result.Add(f);
            }
            return result;
        }

        private async void FoldersList_ItemTapped(object sender, ItemTappedEventArgs e)
        {
            if (this.user == null)
                await DisplayAlert("Usuário","Usuário inválido.", "OK");

            var folder = e.Item as Folder;
            var folders = await this.GetFolders(this?.user, int.Parse(folder?.Id ?? "0"));

            foreach(var f in folders)
            {
                System.Diagnostics.Debug.WriteLine(f.Id);
            }
        }
    }
}
