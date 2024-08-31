using SQLite;

namespace Models
{
    public class Folder
    {
        [PrimaryKey]
        public String? Id { get; set; }
        public String? Name { get; set; }
    }
}
