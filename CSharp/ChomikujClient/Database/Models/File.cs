using SQLite;

namespace Models
{
    public class File
    {
        [PrimaryKey]
        public Int64 ID { get; set; }
        public String Name { get; set; }
        public Int64 ParentID { get; set; }
        public Int64 Size { get; set; }
        public String URL { get; set; }
    }
}
