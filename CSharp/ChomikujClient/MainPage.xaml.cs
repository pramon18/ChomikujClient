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

        private async void LoginBtn_Clicked(object sender, EventArgs e)
        {
            System.Diagnostics.Debug.WriteLine(settings.User.User, settings.User.Password);

            this.user = await new ChomikAPI().Login(settings.User.User, settings.User.Password);

            var f = await new ChomikAPI().GetFolders(this.user, 0);

            f = await SaveFolders(f);

            this.folders = new ObservableCollection<Folder>(f);

            FoldersList.ItemsSource = this.folders;
        }

        private async Task<List<Folder>> SaveFolders(List<Folder> folders)
        {
            List<Folder> result = new List<Folder>();

            // Criar pasta raiz
            var root = new Folder() { ID = 0, Name = this.user.Name, Path = "/" + this.user.Name };

            DB.Connection.InsertOrReplaceAsync(root).Wait();

            result.Add(root);

            // Criar métodos para login e buscar arquivos
            foreach (var f in folders)
            {
                Folder folder = new Folder() { ID = f.ID, Name = f.Name, Path = root.Path + "/" + f.Name };
                DB.Connection.InsertOrReplaceAsync(folder).Wait();
                result.Add(folder);
            }

            return result;
        }

        

        private async void FoldersList_ItemTapped(object sender, ItemTappedEventArgs e)
        {
            if (this.user == null)
                await DisplayAlert("Usuário", "Usuário inválido.", "OK");

            var folder = e.Item as Folder;
            var subFolders = await new ChomikAPI().GetFolders(this.user, folder.ID);
            var files = await new ChomikAPI().GetFiles(this.user, folder.Path);


            foreach (var f in subFolders)
            {
                Folder subFolder = new Folder() { ID = f.ID, Name = f.Name, Path = folder.Path + "/" + f.Name };
                System.Diagnostics.Debug.WriteLine(subFolder.ID.ToString(), subFolder.Name, subFolder.Path);
                DB.Connection.InsertOrReplaceAsync(subFolder).Wait();
            }

            foreach (var f in files)
            {
                System.Diagnostics.Debug.WriteLine(f.ID, f.Name);
                DB.Connection.InsertOrReplaceAsync(f).Wait();
            }
        }
    }
}
