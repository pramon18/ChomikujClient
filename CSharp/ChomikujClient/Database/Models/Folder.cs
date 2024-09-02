using SQLite;

namespace Models
{
    public class Folder
    {
        [PrimaryKey]
        public Int64 ID { get; set; }
        public String? Name { get; set; }
        public String? Path { get; set; }
        public Int64? ParentID {  get; set; }
    }
}
