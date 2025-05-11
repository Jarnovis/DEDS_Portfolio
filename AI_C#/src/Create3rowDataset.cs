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
    ['A'] = new double[] { 
        1, 0, 0,
        0, 0, 0,
        0, 0, 0
    },
    ['B'] = new double[] { 
        0, 1, 0,
        0, 0, 0,
        0, 0, 0
    },
    ['C'] = new double[] { 
        0, 0, 1,
        0, 0, 0,
        0, 0, 0
    },
    ['D'] = new double[] { 
        0, 0, 0,
        1, 0, 0,
        0, 0, 0
    },
    ['E'] = new double[] { 
        0, 0, 0,
        0, 1, 0,
        0, 0, 0
    },
    ['F'] = new double[] { 
        0, 0, 0,
        0, 0, 1,
        0, 0, 0
    },
    ['G'] = new double[] { 
        0, 0, 0,
        0, 0, 0,
        1, 0, 0
    },
    ['H'] = new double[] { 
        0, 0, 0,
        0, 0, 0,
        0, 1, 0
    },
    ['I'] = new double[] { 
        0, 0, 0,
        0, 0, 0,
        0, 0, 1
    },
    ['J'] = new double[] { 
        1, 1, 0,
        0, 0, 0,
        0, 0, 0
    },
    ['K'] = new double[] { 
        0, 1, 1,
        0, 0, 0,
        0, 0, 0
    },
    ['L'] = new double[] { 
        0, 0, 1,
        1, 0, 0,
        0, 0, 0
    },
    ['M'] = new double[] { 
        0, 0, 0,
        1, 1, 0,
        0, 0, 0
    },
    ['N'] = new double[] { 
        0, 0, 0,
        0, 1, 1,
        0, 0, 0
    },
    ['O'] = new double[] { 
        0, 0, 0,
        0, 0, 1,
        1, 0, 0
    },
    ['P'] = new double[] { 
        0, 0, 0,
        0, 0, 0,
        1, 1, 0
    },
    ['Q'] = new double[] { 
        0, 0, 0,
        0, 0, 0,
        0, 1, 1
    },
    ['R'] = new double[] { 
        1, 0, 0,
        0, 0, 0,
        0, 0, 1
    },
    ['S'] = new double[] { 
        1, 1, 1,
        0, 0, 0,
        0, 0, 0
    },
    ['T'] = new double[] { 
        0, 1, 1,
        1, 0, 0,
        0, 0, 0 
    },
    ['U'] = new double[] { 
        0, 0, 1,
        1, 1, 0,
        0, 0, 0
    },
    ['V'] = new double[] { 
        0, 0, 0,
        1, 1, 1,
        0, 0, 0
    },
    ['W'] = new double[] { 
        0, 0, 0,
        0, 1, 1,
        1, 0, 0
    },
    ['X'] = new double[] { 
        0, 0, 0,
        0, 0, 1,
        1, 1, 0
    },
    ['Y'] = new double[] { 
        0, 0, 0,
        0, 0, 0,
        1, 1, 1
    },
    ['Z'] = new double[] { 
        1, 0, 0,
        0, 0, 0,
        0, 1, 1
    },
    ['0'] = new double[] { 
        1, 1, 0,
        0, 0, 0,
        0, 0, 1
    },
    ['1'] = new double[] { 
        1, 1, 1,
        1, 0, 0,
        0, 0, 0
    },
    ['2'] = new double[] { 
        0, 1, 1,
        1, 1, 0,
        0, 0, 0
    },
    ['3'] = new double[] { 
        0, 0, 1,
        1, 1, 1,
        0, 0, 0
    },
    ['4'] = new double[] { 
        0, 0, 0,
        1, 1, 1,
        1, 0, 0
    },
    ['5'] = new double[] { 
        0, 0, 0,
        0, 1, 1,
        1, 1, 0
    },
    ['6'] = new double[] { 
        0, 0, 0,
        0, 0, 1,
        1, 1, 1
    },
    ['7'] = new double[] { 
        1, 0, 0,
        0, 0, 0,
        1, 1, 1
    },
    ['8'] = new double[] { 
        1, 1, 0,
        0, 0, 0,
        0, 1, 1
    },
    ['9'] = new double[] { 
        1, 1, 1,
        0, 0, 0,
        0, 0, 1
    }
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
