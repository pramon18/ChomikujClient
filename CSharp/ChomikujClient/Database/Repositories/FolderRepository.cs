using Database;
using Models;

namespace Repositories
{
    public class FolderRepository
    {
        public FolderRepository() { }

        public async Task CreateOrUpdate(Folder folder)
        {
            var sql = @"SELECT * FROM Folder WHERE Folder.ID = ?";
            var folderDB = (await DB.Connection.QueryAsync<Folder>(sql, folder.ID)).FirstOrDefault();

            // Não permitir alterar path ou pasta parente
            if (folderDB != null) 
            { 
                folder.ParentID = folderDB.ParentID;
            }

            await DB.Connection.InsertOrReplaceAsync(folder);
        }

        public async Task<Folder?> GetFoldersByID(Int64 ID)
        {
            var sql = @"SELECT * FROM Folder WHERE Folder.ID = ?";
            return (await DB.Connection.QueryAsync<Folder>(sql, ID)).FirstOrDefault();
        }

        public async Task<List<Folder>> GetFoldersByParentID(Int64 parentID)
        {
            var sql = @"SELECT * FROM Folder WHERE Folder.ParentID = ?";
            return (await DB.Connection.QueryAsync<Folder>(sql, parentID)).ToList();
        }

        public async Task<int> QtdFolderEmptyPath()
        {
            var sql = @"SELECT * FROM Folder WHERE Folder.Path IS NULL";
            return (await DB.Connection.QueryAsync<Folder>(sql)).Count();
        }
    }
}
