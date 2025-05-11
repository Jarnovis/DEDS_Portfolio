namespace AI;

using System;
using System.Collections.Generic;
using System.Linq;

public class NeuralNetwork
{
    const int inputNodes = 9;
    const int hiddenNodes1 = 72;
    const int hiddenNodes2 = 18;
    const int outputNodes = 36;
    // Snelheid leren
    const double learningRate = 0.01;
    // Aantal herhalingen
    const int epochs = 3000;

    // Gewicht matrixes tussen lagen
    static readonly double[,] W1 = new double[inputNodes, hiddenNodes1];
    static readonly double[,] W2 = new double[hiddenNodes1, hiddenNodes2];
    static readonly double[,] W3 = new double[hiddenNodes2, outputNodes];

    // Biases per laag
    static readonly double[] B1 = new double[hiddenNodes1];
    static readonly double[] B2 = new double[hiddenNodes2];
    static readonly double[] B3 = new double[outputNodes];

    static readonly Random rnd = new();

    // Gewichten en biases worden willekeurig geïnitialiseerd tussen -1 en 1
    static void InitializeWeights()
    {
        static void Init(double[,] M)
        {
            for (int i = 0; i < M.GetLength(0); i++)
                for (int j = 0; j < M.GetLength(1); j++)
                    M[i, j] = rnd.NextDouble() * 2 - 1;
        }

        Init(W1); Init(W2); Init(W3);
        for (int i = 0; i < B1.Length; i++) B1[i] = rnd.NextDouble() * 2 - 1;
        for (int i = 0; i < B2.Length; i++) B2[i] = rnd.NextDouble() * 2 - 1;
        for (int i = 0; i < B3.Length; i++) B3[i] = rnd.NextDouble() * 2 - 1;
    }

    // Voor verborgen lagen
    static double Sigmoid(double x) => 1 / (1 + Math.Exp(-x));
    
    // Voor de outputlaag om waarschijnlijkheden te krijgen
    static double SigmoidDeriv(double y) => y * (1 - y);

    // Nodig voor backpropagation
    static double[] Softmax(double[] z)
    {
        var m = z.Max();
        var ex = z.Select(v => Math.Exp(v - m)).ToArray();
        var sum = ex.Sum();
        return ex.Select(v => v / sum).ToArray();
    }

    // Willekeurige invoer pixels om beter te kunnen werken met ruis
    static void FlipPixels(double[] v, double pct = 0.2)
    {
        int flips = (int)(v.Length * pct);
        for (int i = 0; i < flips; i++)
        {
            int idx = rnd.Next(v.Length);
            v[idx] = v[idx] > 0.5 ? 0 : 1;
        }
    }

    // X => input date (3x3)
    // Y => correcte labels
    public static void Create(IList<double[]> X, IList<double[]> Y)
    {
        // Alle gewichten en biases worden geïnitaliseerd met willekeurig waarden tussen -1 en 1
        InitializeWeights();

        IList<double[]> xReal = X.Select(x => (double[])x.Clone()).ToList();
        IList<double[]> yReal = Y.Select(y => (double[])y.Clone()).ToList();


        for (int epoch = 0; epoch < epochs; epoch++)
        {
            double epochError = 0;

            // Loop over alle trainings voorbeelden
            for (int n = 0; n < X.Count; n++)
            {
                // Toevoegen van 40% ruis aan afbeeldingen
                var x0 = (double[])X[n].Clone();
                FlipPixels(x0, 0.4);

                var h1 = new double[hiddenNodes1];

                // Verbogen laag 1
                // Berekenen activaties voor hiddenNodes1 aantal met sigmoid 
                for (int i = 0; i < hiddenNodes1; i++)
                {
                    for (int j = 0; j < inputNodes; j++)
                        h1[i] += x0[j] * W1[j, i];
                    h1[i] = Sigmoid(h1[i] + B1[i]);
                }

                var h2 = new double[hiddenNodes2];
                // Verbogen laag 2
                // Berekenen activaties voor hiddenNodes2 aantal met sigmoid 
                for (int i = 0; i < hiddenNodes2; i++)
                {
                    for (int j = 0; j < hiddenNodes1; j++)
                        h2[i] += h1[j] * W2[j, i];
                    h2[i] = Sigmoid(h2[i] + B2[i]);
                }

                var o = new double[outputNodes];
                // Berekenen uitoer voor alle output classes
                for (int i = 0; i < outputNodes; i++)
                {
                    for (int j = 0; j < hiddenNodes2; j++)
                        o[i] += h2[j] * W3[j, i];
                    o[i] += B3[i];
                }

                // Zet uitvoer om in kansverdeling van de output classes
                var yHat = Softmax(o);

                // CROSS-ENTROPY error
                var dO = new double[outputNodes];
                for (int i = 0; i < outputNodes; i++)
                {
                    // Fout output
                    dO[i] = yHat[i] - Y[n][i];

                    // Opslaan fout
                    epochError += -Y[n][i] * Math.Log(yHat[i] + 1e-15); 
                }

                // BACKPROP into W3/B3
                var dH2 = new double[hiddenNodes2];
                // Past gewichten en biases aan op basis van de fout
                for (int i = 0; i < hiddenNodes2; i++)
                {
                    for (int k = 0; k < outputNodes; k++)
                        dH2[i] += dO[k] * W3[i, k];
                    dH2[i] *= SigmoidDeriv(h2[i]);
                }

                for (int i = 0; i < hiddenNodes2; i++)
                    for (int k = 0; k < outputNodes; k++)
                        // Berekenen van fout dO terug naar dh2 en pas gewichten aan
                        W3[i, k] -= learningRate * dO[k] * h2[i];
                for (int k = 0; k < outputNodes; k++)
                    B3[k] -= learningRate * dO[k];

                // BACKPROP into W2/B2
                var dH1 = new double[hiddenNodes1];
                for (int i = 0; i < hiddenNodes1; i++)
                {
                    for (int k = 0; k < hiddenNodes2; k++)
                        // Berekenen DH1
                        dH1[i] += dH2[k] * W2[i, k];
                    dH1[i] *= SigmoidDeriv(h1[i]);
                }
                for (int i = 0; i < hiddenNodes1; i++)
                    for (int k = 0; k < hiddenNodes2; k++)
                        W2[i, k] -= learningRate * dH2[k] * h1[i];
                for (int k = 0; k < hiddenNodes2; k++)
                    B2[k] -= learningRate * dH2[k];

                // BACKPROP into W1/B1
                for (int i = 0; i < inputNodes; i++)
                    for (int k = 0; k < hiddenNodes1; k++)
                        W1[i, k] -= learningRate * dH1[k] * x0[i];
                for (int k = 0; k < hiddenNodes1; k++)
                    B1[k] -= learningRate * dH1[k];
            }

            if (epoch % 100 == 0 || epoch == epochs - 1)
                Console.WriteLine($"Epoch {epoch}, Cross-Entropy: {(epochError / X.Count):F4}");
        }

        // EVALUATION (no noise)
        // Opnieuw uitvoeren op originele input
        // Bereken verspelling met de hoogste kans
        // Vergelijken voorspelling (pred) met realiteit (n)
        // Berekenen nauwkeurigheid
        Console.WriteLine("\nResults:");
        int correct = 0;
        for (int n = 0; n < xReal.Count; n++)
        {
            var x0 = X[n];
            var h1 = new double[hiddenNodes1];
            for (int i = 0; i < hiddenNodes1; i++)
            {
                for (int j = 0; j < inputNodes; j++)
                    h1[i] += x0[j] * W1[j, i];
                h1[i] = Sigmoid(h1[i] + B1[i]);
            }

            var h2 = new double[hiddenNodes2];
            for (int i = 0; i < hiddenNodes2; i++)
            {
                for (int j = 0; j < hiddenNodes1; j++)
                    h2[i] += h1[j] * W2[j, i];
                h2[i] = Sigmoid(h2[i] + B2[i]);
            }

            var o = new double[outputNodes];
            for (int i = 0; i < outputNodes; i++)
            {
                for (int j = 0; j < hiddenNodes2; j++)
                    o[i] += h2[j] * W3[j, i];
                o[i] += B3[i];
            }

            var yHat = Softmax(o);
            int pred = Array.IndexOf(yHat, yHat.Max());
            
            int real = Array.IndexOf(Y[n], 1.0);
            if (pred == real) correct++;

            if (pred != real)
                for (int i = 0; i < yHat.Length; i++)
                    Console.WriteLine($"Class {i}: {yHat[i]:F3}");

            Console.WriteLine($"Input #{n}: Pred={pred}, Real={n}, Conf={yHat[pred]:F3}");
        }

        Console.WriteLine($"Accuracy: {100.0 * correct / X.Count:F2}%");
    }
}
