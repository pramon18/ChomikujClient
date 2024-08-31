using Models;
using System.Text;
using System.Xml.Linq;
using Util;

namespace ChomikujClient.API
{
    public class ChomikAPI
    {
        // URL das requisições
        private string URL = "http://box.chomikuj.pl/services/ChomikBoxService.svc";

        List<String> actions = new List<String>() { "Auth", "Folders" };

        private HttpClient _httpClient;

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

        public async Task<User> Login(string username, string password)
        {
            System.Diagnostics.Debug.WriteLine(username, HashUtil.ComputeMD5(password).ToLower());

            // Login
            var content = @$"<Auth xmlns=""http://chomikuj.pl/"">
			                    <name>{username}</name>
			                    <passHash>{HashUtil.ComputeMD5(password).ToLower()}</passHash>
			                    <client>
				                    <name>chomikbox</name>
				                    <version>2.0.8.2</version>
			                    </client>
                                <ver>4</ver>
                            </Auth>";

            // Montar requisição
            SOAPRequest request = new SOAPRequest(this.URL, content);

            request.headers.Add("SOAPAction", "http://chomikuj.pl/IChomikBoxService/Auth");

            var response = await this.SendSoapRequest(request);

            XDocument doc = XDocument.Parse(response);

            // Carregar no objeto
            User user = new User();

            var status = XMLUtil.GetValueByName(doc, "status");
            user.ChomikID = XMLUtil.GetValueByName(doc, "hamsterId");
            user.Name = XMLUtil.GetValueByName(doc, "name");
            user.Token = XMLUtil.GetValueByName(doc, "token");

            return user;
        }

        public async Task<List<Folder>> GetFolders(User user, int folderID, int depth = 2)
        {
            List<Folder> result = new List<Folder>();

            // USAR URL DO CHOMIKBOX como base
            var Url = "http://box.chomikuj.pl/services/ChomikBoxService.svc";

            // NESSE PONTO DEVO TER UM USUÁRIO LOGADO
            // TENTAR PEGAR PASTAS
            var content = @$"<Folders xmlns=""http://chomikuj.pl/"">
                           <token>{user.Token}</token>
                           <hamsterId>{user.ChomikID}</hamsterId>
                           <folderId>{folderID}</folderId>
                           <depth>{depth}</depth>
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

                this._content = this.soapEnvelope.ToString();
            }
        }
    }
}
