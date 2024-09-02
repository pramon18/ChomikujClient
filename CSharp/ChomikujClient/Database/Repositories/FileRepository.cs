using Database;
using Models;

namespace Repositories
{
    public class FileRepository
    {
        public async Task CreateOrUpdate(Models.File file)
        {
            var sql = @"SELECT * FROM File WHERE File.ID = ?";
            var fileDB = (await DB.Connection.QueryAsync<Folder>(sql, file.ID)).FirstOrDefault();

            // Não permitir alterar pasta parente
            if (fileDB != null)
            {
                fileDB.ParentID = fileDB.ParentID;
            }

            await DB.Connection.InsertOrReplaceAsync(file);
        }
    }
}
