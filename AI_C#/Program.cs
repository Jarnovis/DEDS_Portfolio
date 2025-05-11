namespace AI;

using System.Reflection.Metadata;

public static class Program
{
    public static void Main(string[] args)
    {
        (IList<double[]> Images, IList<double[]> Labels) dataset = Create3RowDataset.GenerateSymbolicImageDataset();
        NeuralNetwork.Create(dataset.Images, dataset.Labels);
    }
}