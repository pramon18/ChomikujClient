using Models;

namespace Services.Interfaces
{
    public interface IAPIService
    {
        Task<List<Models.File>> GetFiles(User user, Folder folder);
        Task<FolderResult> GetFolders(User user, long folderID, int depth = 2);
        Task<User> Login(string username, string password);
    }
}