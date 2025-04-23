namespace CSharp_xUnit_starter;

public class Rover
{
    public Coordinates Coordinates { get; }

    public Rover(int x, int y, Direction direction)
    {
        Coordinates = new Coordinates(x, y, direction);
    }
    // with { Rover = this };

    public Rover(Coordinates coordinates)
    {
        Coordinates = coordinates;
    }

    public Rover Advance()
    {
        return Coordinates.Direction switch
        {
            Direction.North => new Rover(Coordinates.YTranslate()),
            Direction.South => new Rover(Coordinates.YAntiTranslate()),
            Direction.West => new Rover(Coordinates.XAntiTranslate()),
            Direction.East => new Rover(Coordinates.XTranslate()),
            _ => throw new ArgumentOutOfRangeException()
        };
    }
    public Rover Back()
    {
        return Coordinates.Direction switch
        {
            Direction.North => new Rover(Coordinates.YAntiTranslate()),
            Direction.South => new Rover(Coordinates.YTranslate()),
            Direction.West => new Rover(Coordinates.XTranslate()),
            Direction.East => new Rover(Coordinates.XAntiTranslate()),
            _ => throw new ArgumentOutOfRangeException()
        };
    }

    public Rover AntiRotate()
    {
        return new Rover(Coordinates.AntiRotate());
    }

    public Rover Rotate()
    {
        return new Rover(Coordinates.Rotate());
    }
}