class Program
{
    static void Main(string[] args)
    {
        var lines = File.ReadAllLines("../input.txt");

        int counter = 50;
        int roll = 0;

        foreach (var line in lines)
        {
            int direction = line[0] == 'R' ? 1 : -1;

            int amount = int.Parse(line[1..]);

            counter = ((counter % 100) + 100) % 100;
            counter += direction * amount;

            int q = (int)Math.Floor(counter / 100.0);
            roll += Math.Abs(q);
        }

        Console.WriteLine($"Answer: {roll}");
    }
}