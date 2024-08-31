using ChomikujClient.API;
using CommunityToolkit.Maui.Alerts;
using CommunityToolkit.Maui.Core;
using CommunityToolkit.Maui.Storage;
using Database;
using Microsoft.Extensions.Configuration;
using Models;
using System.Collections.ObjectModel;
using static ChomikujClient.MauiProgram;

namespace ChomikujClient
{
    public partial class MainPage : ContentPage
    {
        int count = 0;

        private string path;
        private HttpClient _httpClient = new HttpClient();
        private ObservableCollection<Folder> folders = new ObservableCollection<Folder>();
        private User? user = null;

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

        public class Chomik
        {
            public String name { get; set; } = String.Empty;
            public String token { get; set; } = String.Empty;
            public String chomikId { get; set; } = String.Empty;
        }

        private async void LoginBtn_Clicked(object sender, EventArgs e)
        {
            System.Diagnostics.Debug.WriteLine(settings.User.User, settings.User.Password);

            this.user = await new ChomikAPI().Login(settings.User.User, settings.User.Password);

            this.folders = new ObservableCollection<Folder>(await new ChomikAPI().GetFolders(this.user, 0));

            FoldersList.ItemsSource = this.folders;

            // Criar métodos para login e buscar arquivos
            foreach (var f in this.folders)
            {
                var folder = new Folder() { Id = f.Id, Name = f.Name };
                DB.Connection.InsertOrReplaceAsync(folder).Wait();
            }
        }

        //private async Task<List<Folder>> GetFolders(User user, int folderId = 0)
        //{
        //    List<Folder> result = new List<Folder>();

        //    // USAR URL DO CHOMIKBOX como base
        //    var Url = "http://box.chomikuj.pl/services/ChomikBoxService.svc";

        //    // NESSE PONTO DEVO TER UM USUÁRIO LOGADO
        //    // TENTAR PEGAR PASTAS
        //    var content = @$"<Folders xmlns=""http://chomikuj.pl/"">
        //               <token>{user.Token}</token>
        //               <hamsterId>{user.ChomikID}</hamsterId>
        //               <folderId>{folderId}</folderId>
        //               <depth>2</depth>
        //              </Folders>";

        //    // Depth 2 pega a primeira fileira, igual aparece no site.
        //    // Depth 0 pega tudo.

        //    SOAPRequest request = new SOAPRequest(Url, content);
        //    request.headers.Add("SOAPAction", "http://chomikuj.pl/IChomikBoxService/Folders");

        //    var response = await this.SendSoapRequest(request);

        //    XDocument doc = XDocument.Parse(response);

        //    var folders = XMLUtil.GetElementsByName(doc, "FolderInfo");

        //    foreach (var folder in folders)
        //    {
        //        var id = XMLUtil.GetValueByName(folder, "id");
        //        var name = XMLUtil.GetValueByName(folder, "name");
        //        Folder f = new Folder() { Id = id, Name = name };
        //        result.Add(f);
        //    }
        //    return result;
        //}

        private async void FoldersList_ItemTapped(object sender, ItemTappedEventArgs e)
        {
            return;
            //if (this.user == null)
            //    await DisplayAlert("Usuário", "Usuário inválido.", "OK");

            //var folder = e.Item as Folder;
            //var folders = await this.GetFolders(this?.user, int.Parse(folder?.Id ?? "0"));

            //foreach (var f in folders)
            //{
            //    System.Diagnostics.Debug.WriteLine(f.Id);
            //}
        }
    }
}
