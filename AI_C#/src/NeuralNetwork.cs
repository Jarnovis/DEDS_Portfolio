// namespace AI;

// using System;
// using System.Collections.Generic;

// public class NeuralNetwork
// {
//     /// <summary>
//     /// Benodigde groote lijst input
//     /// </summary>
//     const int inputNodes = 4;
//     /// <summary>
//     /// Verstopte Neurons
//     /// </summary>
//     const int hiddenNodes = 5;
//     /// <summary>
//     /// Output (0 - 1)
//     /// </summary>
//     const int outputNodes = 1;
//     /// <summary>
//     /// Leersnelheid voor precie (nu 10%)
//     /// </summary>
//     const double learningRate = 0.1;
//     /// <summary>
//     /// Hoevaak een dataset wordt herhaald (te hoge epochs zorgt voor overfitting)
//     /// </summary>
//     const int epochs = 5000;

//     /// <summary>
//     /// 2D Array<br/>
//     /// Elk element staat voor een gewicht dat de sterkte bepaald tussen één specifieke input node en één specifice hidden node.</br>
//     /// Wanneer een netwerk getrained wordt, worden deze gewichten aangepast om minimale errors te voorkomen in de output.
//     /// </summary>
//     static double[,] weightsInputHidden = new double[inputNodes, hiddenNodes];
//     /// <summary>
//     /// 1D Array<br/>
//     /// Elk element representeerd een bias voor een specifieke verstope node.<br/>
//     /// De Bias is toegevoegd aan het gewicht van de som van de inputs van die hidden node.<br/>
//     /// Het doel is om het model beter de data toe te passen voor de activatie.<br/>
//     /// Each element in this array represents a bias for a specific hidden node.<br/>
//     /// Biases worden ook geleerd tijdens training.
//     /// </summary>
//     static double[] biasHidden = new double[hiddenNodes];
//     /// <summary>
//     /// 2D Array<br/>
//     /// Elk element in de array vertegenwoordig een gewicht dat verbonden is met een specifieke hidden node naar de output node.<br/>
//     /// Net zoals de weightsInputHidden, zijn deze gewichten bepaald op hoeveel de invloed van elke hidden node is op de uiteindelijke output.<br/>
//     /// Tijdens trainen, worden deze gewichten aangepast.
//     /// </summary>
//     static double[,] weightsHiddenOutput = new double[hiddenNodes, outputNodes];
//     /// <summary>
//     /// 1D Array<br/>
//     /// Arrat bev
//     /// This array contains a single bias value for the output node.
//     /// The bias is added to the weighted sum of the hidden nodes' outputs before passing it through the activation function (in this case, the sigmoid function).
//     /// The bias allows the output to shift in order to better match the target labels during training.
//     /// </summary>
//     static double[] biasOutput = new double[outputNodes];

//     static Random rand = new Random();

//     static void InitializeWeights()
//     {
//         for (int i = 0; i < inputNodes; i++)
//             for (int j = 0; j < hiddenNodes; j++)
//                 weightsInputHidden[i, j] = rand.NextDouble() * 2 - 1;

//         for (int j = 0; j < hiddenNodes; j++)
//             weightsHiddenOutput[j, 0] = rand.NextDouble() * 2 - 1;

//         for (int j = 0; j < hiddenNodes; j++)
//             biasHidden[j] = rand.NextDouble() * 2 - 1;

//         biasOutput[0] = rand.NextDouble() * 2 - 1;
//     }

//     static double Sigmoid(double x) => 1 / (1 + Math.Exp(-x));

//     static double SigmoidDerivative(double x) => x * (1 - x);

//     public static void Create()
//     {
//         InitializeWeights();

//         // Trainingsdata
//         List<double[]> inputs = new List<double[]>
//         {
//             new double[] {0, 0, 0, 1},
//             new double[] {1, 1, 0, 0},
//             new double[] {1, 0, 1, 1},
//             new double[] {0, 1, 1, 0},
//             new double[] {1, 1, 1, 1}
//         };
//         double[] labels = { 0, 1, 1, 0, 1 };

//         for (int epoch = 0; epoch < epochs; epoch++)
//         {
//             double totalError = 0;
//             for (int i = 0; i < inputs.Count; i++)
//             {
//                 double[] input = inputs[i];
//                 double target = labels[i];

//                 // --- Forward ---
//                 double[] hiddenInputs = new double[hiddenNodes];
//                 for (int j = 0; j < hiddenNodes; j++)
//                 {
//                     for (int k = 0; k < inputNodes; k++)
//                         hiddenInputs[j] += input[k] * weightsInputHidden[k, j];
//                     hiddenInputs[j] += biasHidden[j];
//                     hiddenInputs[j] = Sigmoid(hiddenInputs[j]);
//                 }

//                 double output = 0;
//                 for (int j = 0; j < hiddenNodes; j++)
//                     output += hiddenInputs[j] * weightsHiddenOutput[j, 0];
//                 output += biasOutput[0];
//                 output = Sigmoid(output);

//                 double error = target - output;
//                 totalError += error * error;

//                 // --- Backpropagation ---
//                 double dOutput = error * SigmoidDerivative(output);

//                 // Hidden-output updates
//                 for (int j = 0; j < hiddenNodes; j++)
//                     weightsHiddenOutput[j, 0] += learningRate * dOutput * hiddenInputs[j];
//                 biasOutput[0] += learningRate * dOutput;

//                 // Hidden layer updates
//                 double[] dHidden = new double[hiddenNodes];
//                 for (int j = 0; j < hiddenNodes; j++)
//                 {
//                     dHidden[j] = dOutput * weightsHiddenOutput[j, 0] * SigmoidDerivative(hiddenInputs[j]);
//                     for (int k = 0; k < inputNodes; k++)
//                         weightsInputHidden[k, j] += learningRate * dHidden[j] * input[k];
//                     biasHidden[j] += learningRate * dHidden[j];
//                 }
//             }

//             if (epoch % 500 == 0)
//                 Console.WriteLine($"Epoch {epoch}, MSE: {totalError / inputs.Count:F4}");
//         }

//         // --- Testen ---
//         Console.WriteLine("\nResultaten:");
//         foreach (var input in inputs)
//         {
//             double[] hidden = new double[hiddenNodes];
//             for (int j = 0; j < hiddenNodes; j++)
//             {
//                 for (int k = 0; k < inputNodes; k++)
//                     hidden[j] += input[k] * weightsInputHidden[k, j];
//                 hidden[j] += biasHidden[j];
//                 hidden[j] = Sigmoid(hidden[j]);
//             }

//             double output = 0;
//             for (int j = 0; j < hiddenNodes; j++)
//                 output += hidden[j] * weightsHiddenOutput[j, 0];
//             output += biasOutput[0];
//             output = Sigmoid(output);

//             Console.WriteLine($"Input: [{string.Join(", ", input)}] => Output: {output:F4}");
//         }
//     }
// }


namespace AI;

using System;
using System.Collections.Generic;

public class NeuralNetwork
{
    const int inputNodes = 4;
    const int hiddenNodes = 5;
    const int outputNodes = 1;
    const double learningRate = 0.1;
    const int epochs = 3550;
    static double[,] weightsInputHidden = new double[inputNodes, hiddenNodes];
    static double[] biasHidden = new double[hiddenNodes];
    static double[,] weightsHiddenOutput = new double[hiddenNodes, outputNodes];
    static double[] biasOutput = new double[outputNodes];

    static Random rand = new Random();

    static void InitializeWeights()
    {
        for (int i = 0; i < inputNodes; i++)
            for (int j = 0; j < hiddenNodes; j++)
                weightsInputHidden[i, j] = rand.NextDouble() * 2 - 1;

        for (int j = 0; j < hiddenNodes; j++)
            weightsHiddenOutput[j, 0] = rand.NextDouble() * 2 - 1;

        for (int j = 0; j < hiddenNodes; j++)
            biasHidden[j] = rand.NextDouble() * 2 - 1;

        biasOutput[0] = rand.NextDouble() * 2 - 1;
    }

    static double Sigmoid(double x) => 1 / (1 + Math.Exp(-x));

    static double SigmoidDerivative(double x) => x * (1 - x);

    public static void Create()
    {
        InitializeWeights();

        // Trainingsdata
        List<double[]> inputs = new List<double[]>
        {
            new double[] {0, 0, 0, 1},
            new double[] {1, 1, 0, 0},
            new double[] {1, 0, 1, 1},
            new double[] {0, 1, 1, 0},
            new double[] {1, 1, 1, 1}
        };

        double[] labels = [0, 1, 1, 0, 1];

        for (int epoch = 0; epoch < epochs; epoch++)
        {
            double totalError = 0;
            for (int i = 0; i < inputs.Count; i++)
            {
                double[] input = inputs[i];
                double target = labels[i];

                // --- Forward ---
                double[] hiddenInputs = new double[hiddenNodes];
                for (int j = 0; j < hiddenNodes; j++)
                {
                    for (int k = 0; k < inputNodes; k++)
                        hiddenInputs[j] += input[k] * weightsInputHidden[k, j];
                    hiddenInputs[j] += biasHidden[j];
                    hiddenInputs[j] = Sigmoid(hiddenInputs[j]);
                }

                double output = 0;
                for (int j = 0; j < hiddenNodes; j++)
                    output += hiddenInputs[j] * weightsHiddenOutput[j, 0];
                output += biasOutput[0];
                output = Sigmoid(output);

                double error = target - output;
                totalError += error * error;

                // --- Backpropagation ---
                double dOutput = error * SigmoidDerivative(output);

                // Hidden-output updates
                for (int j = 0; j < hiddenNodes; j++)
                    weightsHiddenOutput[j, 0] += learningRate * dOutput * hiddenInputs[j];
                biasOutput[0] += learningRate * dOutput;

                // Hidden layer updates
                double[] dHidden = new double[hiddenNodes];
                for (int j = 0; j < hiddenNodes; j++)
                {
                    dHidden[j] = dOutput * weightsHiddenOutput[j, 0] * SigmoidDerivative(hiddenInputs[j]);
                    for (int k = 0; k < inputNodes; k++)
                        weightsInputHidden[k, j] += learningRate * dHidden[j] * input[k];
                    biasHidden[j] += learningRate * dHidden[j];
                }
            }

            if (epoch % 500 == 0)
                Console.WriteLine($"Epoch {epoch}, MSE: {totalError / inputs.Count:F4}");
        }

        // --- Testen ---
        Console.WriteLine("\nResultaten:");
        foreach (var input in inputs)
        {
            double[] hidden = new double[hiddenNodes];
            for (int j = 0; j < hiddenNodes; j++)
            {
                for (int k = 0; k < inputNodes; k++)
                    hidden[j] += input[k] * weightsInputHidden[k, j];
                hidden[j] += biasHidden[j];
                hidden[j] = Sigmoid(hidden[j]);
            }

            double output = 0;
            for (int j = 0; j < hiddenNodes; j++)
                output += hidden[j] * weightsHiddenOutput[j, 0];
            output += biasOutput[0];
            output = Sigmoid(output);

            Console.WriteLine($"Input: [{string.Join(", ", input)}] => Output: {output:F4}");
        }
    }
}
