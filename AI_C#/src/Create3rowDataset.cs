namespace AI;
public class Create3RowDataset
{
    public static (List<double[]>, List<double[]>) GenerateSymbolicImageDataset()
    {
        Dictionary<char, int> labelsMap = new Dictionary<char, int>();
        List<double[]> images = new List<double[]>();
        List<double[]> labels = new List<double[]>(); 
        
        for (char c = 'A'; c <= 'Z'; c++) labelsMap[c] = labelsMap.Count;
        for (char c = '0'; c <= '9'; c++) labelsMap[c] = labelsMap.Count;

        var charImages = new Dictionary<char, double[]>
        {
            ['A'] = [ 
                1, 0, 0,
                0, 0, 0,
                0, 0, 0
            ],
            ['B'] = [ 
                0, 1, 0,
                0, 0, 0,
                0, 0, 0
            ],
            ['C'] = [ 
                0, 0, 1,
                0, 0, 0,
                0, 0, 0
            ],
            ['D'] = [ 
                0, 0, 0,
                1, 0, 0,
                0, 0, 0
            ],
            ['E'] = [ 
                0, 0, 0,
                0, 1, 0,
                0, 0, 0
            ],
            ['F'] = [ 
                0, 0, 0,
                0, 0, 1,
                0, 0, 0
            ],
            ['G'] = [ 
                0, 0, 0,
                0, 0, 0,
                1, 0, 0
            ],
            ['H'] = [ 
                0, 0, 0,
                0, 0, 0,
                0, 1, 0
            ],
            ['I'] = [ 
                0, 0, 0,
                0, 0, 0,
                0, 0, 1
            ],
            ['J'] = [ 
                1, 1, 0,
                0, 0, 0,
                0, 0, 0
            ],
            ['K'] = [ 
                0, 1, 1,
                0, 0, 0,
                0, 0, 0
            ],
            ['L'] = [ 
                0, 0, 1,
                1, 0, 0,
                0, 0, 0
            ],
            ['M'] = [ 
                0, 0, 0,
                1, 1, 0,
                0, 0, 0
            ],
            ['N'] = [ 
                0, 0, 0,
                0, 1, 1,
                0, 0, 0
            ],
            ['O'] = [ 
                0, 0, 0,
                0, 0, 1,
                1, 0, 0
            ],
            ['P'] = [ 
                0, 0, 0,
                0, 0, 0,
                1, 1, 0
            ],
            ['Q'] = [ 
                0, 0, 0,
                0, 0, 0,
                0, 1, 1
            ],
            ['R'] = [ 
                1, 0, 0,
                0, 0, 0,
                0, 0, 1
            ],
            ['S'] = [ 
                1, 1, 1,
                0, 0, 0,
                0, 0, 0
            ],
            ['T'] = [ 
                0, 1, 1,
                1, 0, 0,
                0, 0, 0 
            ],
            ['U'] = [ 
                0, 0, 1,
                1, 1, 0,
                0, 0, 0
            ],
            ['V'] = [ 
                0, 0, 0,
                1, 1, 1,
                0, 0, 0
            ],
            ['W'] = [ 
                0, 0, 0,
                0, 1, 1,
                1, 0, 0
            ],
            ['X'] = [ 
                0, 0, 0,
                0, 0, 1,
                1, 1, 0
            ],
            ['Y'] = [ 
                0, 0, 0,
                0, 0, 0,
                1, 1, 1
            ],
            ['Z'] = [ 
                1, 0, 0,
                0, 0, 0,
                0, 1, 1
            ],
            ['0'] = [ 
                1, 1, 0,
                0, 0, 0,
                0, 0, 1
            ],
            ['1'] = [ 
                1, 1, 1,
                1, 0, 0,
                0, 0, 0
            ],
            ['2'] = [ 
                0, 1, 1,
                1, 1, 0,
                0, 0, 0
            ],
            ['3'] = [ 
                0, 0, 1,
                1, 1, 1,
                0, 0, 0
            ],
            ['4'] = [ 
                0, 0, 0,
                1, 1, 1,
                1, 0, 0
            ],
            ['5'] = [ 
                0, 0, 0,
                0, 1, 1,
                1, 1, 0
            ],
            ['6'] = [ 
                0, 0, 0,
                0, 0, 1,
                1, 1, 1
            ],
            ['7'] = [ 
                1, 0, 0,
                0, 0, 0,
                1, 1, 1
            ],
            ['8'] = [ 
                1, 1, 0,
                0, 0, 0,
                0, 1, 1
            ],
            ['9'] = [ 
                1, 1, 1,
                0, 0, 0,
                0, 0, 1
            ]
        };



        int p = 0;
        foreach (var kv in charImages)
        {

            images.Add(kv.Value);
            
            double[] oneHotLabel = new double[labelsMap.Count];
            int labelIndex = labelsMap[kv.Key];
            oneHotLabel[labelIndex] = 1.0;

            labels.Add(oneHotLabel);

            Console.WriteLine($"{p++} = {kv.Key}");
        }

        return (images, labels);
    }
}
