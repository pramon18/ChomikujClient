using Models;
using Services.Interfaces;
using System.Text;
using System.Xml.Linq;
using Util;

namespace Services
{
    public class APIService : IAPIService
    {
        private HttpClient _httpClient = null!;

        // URL das requisições
        private string URL = "http://box.chomikuj.pl/services/ChomikBoxService.svc";

        public enum Actions
        {
            Auth,
            Folders,
            Download
        }

        public APIService() { }

        private HttpClient GetClient()
        {
            if (_httpClient == null)
                _httpClient = new HttpClient();

            return this._httpClient;
        }

        private async Task<string> SendSoapRequest(SOAPRequest request)
        {
            foreach (var header in request.headers)
            {
                GetClient().DefaultRequestHeaders.Clear();
                GetClient().DefaultRequestHeaders.Add(header.Key, header.Value);
            }

            HttpContent content = new StringContent(request.Content, Encoding.UTF8, "text/xml");

            HttpResponseMessage response = GetClient().PostAsync(request.url, content).Result;

            return await response.Content.ReadAsStringAsync();
        }

        public async Task<User> Login(string username, string password)
        {
            // Login
            var content = @$"<Auth xmlns=""http://chomikuj.pl/"">
			                    <name>{username}</name>
			                    <passHash>{HashUtil.ComputeMD5(password)}</passHash>
			                    <client>
				                    <name>chomikbox</name>
				                    <version>2.0.8.2</version>
			                    </client>
                                <ver>4</ver>
                            </Auth>";

            // Montar requisição
            SOAPRequest request = new SOAPRequest(URL, content, Actions.Auth);

            var response = await SendSoapRequest(request);

            XDocument doc = XDocument.Parse(response);

            var status = XMLUtil.GetValueByName(doc, "status");

            // Carregar no objeto
            User user = new User()
            {
                ID = Int64.Parse(XMLUtil.GetValueByName(doc, "hamsterId")),
                Name = XMLUtil.GetValueByName(doc, "name"),
                Token = XMLUtil.GetValueByName(doc, "token")
            };

            return user;
        }

        public async Task<FolderResult> GetFolders(User user, long folderID, int depth = 2)
        {
            // Montar corpo
            var content = @$"<Folders xmlns=""http://chomikuj.pl/"">
                               <token>{user.Token}</token>
                               <hamsterId>{user.ID}</hamsterId>
                               <folderId>{folderID}</folderId>
                               <depth>{depth}</depth>
                             </Folders>";

            // Depth 2 pega a primeira fileira, igual aparece no site.
            // Depth 0 pega tudo.

            // Criar requisição
            SOAPRequest request = new SOAPRequest(URL, content, Actions.Folders);

            var response = await SendSoapRequest(request);

            XDocument doc = XDocument.Parse(response);

            // Rota sempre retorna a raiz pesquisada e subpastas se existirem

            FolderResult result = new FolderResult();

            var root = XMLUtil.GetElementByName(doc, "folder");

            result.Root = new Folder()
            {
                ID = long.Parse(XMLUtil.GetValueByName(root, "id")),
                Name = XMLUtil.GetValueByName(root, "name")
            };

            var folders = XMLUtil.GetElementsByName(doc, "FolderInfo");

            foreach (var folder in folders)
            {
                result.Folders.Add(new Folder()
                {
                    ID = long.Parse(XMLUtil.GetValueByName(folder, "id")),
                    Name = XMLUtil.GetValueByName(folder, "name"),
                    ParentID = result.Root.ID
                });
            }
            return result;
        }

        public async Task<List<Models.File>> GetFiles(User user, Folder folder)
        {
            List<Models.File> result = new List<Models.File>();

            // List of Files
            var content = @$"<Download xmlns=""http://chomikuj.pl/"">
			                    <token>{user.Token}</token>
			                    <sequence>
				                    <stamp>0</stamp>
				                    <part>0</part>
				                    <count>1</count>
			                    </sequence>
			                    <disposition>download</disposition>
			                    <list>
				                    <DownloadReqEntry>
					                    <id>{folder.Path}</id>
					                    <agreementInfo>
						                    <AgreementInfo>
							                    <name>own</name>
						                    </AgreementInfo>
					                    </agreementInfo>
				                    </DownloadReqEntry>
			                    </list>
		                    </Download>";

            // Criar requisição
            SOAPRequest request = new SOAPRequest(URL, content, Actions.Download);

            var response = await SendSoapRequest(request);
            XDocument doc = XDocument.Parse(response);

            var files = XMLUtil.GetElementsByName(doc, "FileEntry");

            foreach (var file in files)
            {
                result.Add(new Models.File()
                {
                    ID = long.Parse(XMLUtil.GetValueByName(file, "id")),
                    Name = XMLUtil.GetElementsByName(file, "name").Where(x => x.Value != "own").FirstOrDefault()?.Value!,
                    ParentID = folder.ID,
                    Size = long.Parse(XMLUtil.GetValueByName(file, "size")),
                    URL = XMLUtil.GetValueByName(file, "url"),
                });
            }

            return result;
        }
    }

    public class FolderResult
    {
        public Folder Root { get; set; }
        public List<Folder> Folders { get; set; } = new List<Folder>();

        public List<Folder> GetFolders()
        {
            List<Folder> folders = new List<Folder>();
            folders.Add(Root);
            folders.AddRange(Folders);
            return folders;
        }
    }

    public class SOAPRequest
    {
        public string url { get; set; }
        public Dictionary<string, string> headers { get; set; }
        public XDocument soapEnvelope { get; set; }

        public SOAPRequest(string url, string content, APIService.Actions action)
        {
            // Headers padrão
            headers = new Dictionary<string, string>
            {
                // headers padrão
                { "User-Agent", "Mozilla/5.0" },
                { "Accept-Language", "en-US,*" },
                { "Accept", "*/*" }
            };

            // Headers de acordo com a ação
            switch (action)
            {
                case APIService.Actions.Auth:
                    headers.Add("SOAPAction", "http://chomikuj.pl/IChomikBoxService/Auth");
                    break;
                case APIService.Actions.Folders:
                    headers.Add("SOAPAction", "http://chomikuj.pl/IChomikBoxService/Folders");
                    break;
                case APIService.Actions.Download:
                    headers.Add("SOAPAction", "http://chomikuj.pl/IChomikBoxService/Download");
                    break;
            }

            // Envelope padrão
            soapEnvelope = XDocument.Parse(@"<?xml version=""1.0"" encoding=""utf-8""?>
                                                     <s:Envelope s:encodingStyle=""http://schemas.xmlsoap.org/soap/encoding/"" xmlns:s=""http://schemas.xmlsoap.org/soap/envelope/"">     
                                                        <s:Body>		                    
	                                                    </s:Body>
                                                     </s:Envelope>");
            // Destino e conteúdo
            this.url = url;
            Content = content;
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
                var element = XMLUtil.GetElementByName(soapEnvelope, "Body");
                if (element != null)
                {
                    element.Add(XElement.Parse(value));
                }

                _content = soapEnvelope.ToString();
            }
        }
    }
}
