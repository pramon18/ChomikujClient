using Services;
using CommunityToolkit.Maui.Alerts;
using CommunityToolkit.Maui.Core;
using CommunityToolkit.Maui.Storage;
using Microsoft.Extensions.Configuration;
using Models;
using Repositories;
using System.Collections.ObjectModel;
using static ChomikujClient.MauiProgram;
using Services.Interfaces;

namespace ChomikujClient
{
    public partial class MainPage : ContentPage
    {
        private string path;
        private ObservableCollection<Folder> folders = new ObservableCollection<Folder>();
        private User? user = null;

        private Settings settings = MauiProgram.Services?.GetService<IConfiguration>()?.GetRequiredSection("Settings").Get<Settings>()!;

        private IAPIService _apiService { get; set; }

        public MainPage(IAPIService apiService)
        {
            InitializeComponent();

            this._apiService = apiService;
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

            this.user = await _apiService.Login(settings.User.User, settings.User.Password);
        }

        private async Task<List<Folder>> SaveFolders(List<Folder> folders)
        {
            // Criar métodos para login e buscar arquivos
            foreach (var f in folders)
                await new FolderRepository().CreateOrUpdate(f);

            if (await new FolderRepository().QtdFolderEmptyPath() > 0)
            {
                // Ajustar caminhos de todas as pastas
                var root = await new FolderRepository().GetFoldersByID(0);
                await RestorePath(root, null);
            }           

            return folders;
        }

        private async Task<List<Models.File>> SaveFiles(List<Models.File> files)
        {
            // Criar métodos para login e buscar arquivos
            foreach (var f in files)
                await new FileRepository().CreateOrUpdate(f);

            return files;
        }

        private async void FoldersList_ItemTapped(object sender, ItemTappedEventArgs e)
        {
            if (this.user == null)
                await DisplayAlert("Usuário", "Usuário inválido.", "OK");

            var folder = await new FolderRepository().GetFoldersByID((e.Item as Folder).ID);
            var subFolders = await _apiService.GetFolders(this.user, folder.ID);
            var files = await _apiService.GetFiles(this.user, folder);

            // Salvar pastas
            await SaveFolders(subFolders.GetFolders());

            // Salvar arquivos
            await SaveFiles(files);

            foreach (var f in subFolders.Folders)
            {
                System.Diagnostics.Debug.WriteLine(f.ID.ToString(), f.Name, f.Path);
            }

            foreach (var f in files)
            {
                System.Diagnostics.Debug.WriteLine(f.ID, f.Name);
            }
        }

        private async void BuscarPastasBtn_Clicked(object sender, EventArgs e)
        {
            if (this.user == null)
                await DisplayAlert("Usuário", "Usuário inválido.", "OK");

            var f = await _apiService.GetFolders(this.user, 0);

            await SaveFolders(f.GetFolders());

            this.folders = new ObservableCollection<Folder>(f.GetFolders());

            FoldersList.ItemsSource = this.folders;
        }

        private async Task RestorePath(Folder root, List<Folder> subfolders)
        {
            // Raiz geral
            if (root.ID == 0)
            {
                root.Path = "/" + root.Name;

                await new FolderRepository().CreateOrUpdate(root);

                System.Diagnostics.Debug.WriteLine(root.ID, root.Path);
            }

            // Buscar pastas internas
            subfolders = await new FolderRepository().GetFoldersByParentID(root.ID);

            // Parar quando não houver subpastas
            if (subfolders == null)
                return;

            foreach (var f in subfolders)
            {
                f.Path = root.Path + "/" + f.Name;
                await new FolderRepository().CreateOrUpdate(f);
                System.Diagnostics.Debug.WriteLine(f.ID, f.Path);
                await RestorePath(f, null);
            }
        }
    }
}
