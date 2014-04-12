##Dataset

####DatasetItem

    class DatasetItem
    {
        public sample

        loadFromFile(filename)  // Effectue le pre-processing
        loadFromImage(image)    // Effectue le pre-processing
    }

`sample` : Tableau d'une dimension, contenant toutes les valeurs des pixels de chaque ligne de l'image après pre-processing.

    [ [0 1 0 0]
      [0 1 0 0]
      [0 3 2 0]    =  [0 1 0 0 0 1 0 0 0 3 2 0 0 0 0 0]
      [0 0 0 0] ]

-------------

####Dataset

    class Dataset
    {
        public samples          // Disponible après le pre-processing
        public responses        // Disponible après le pre-processing
        public sampleCount      // Disponible après le pre-processing
        public classCount       // Nombre de classification
        public maxPerClass      // Nombre maximum de samples par classe

        Dataset(folders)
        preprocess()

        getResponse(n)  // Retourne le label de la n-ième classification
    }

-------------

`folders` (hash table) :

    'a': 'dataset/a_small'
    'b': 'dataset/b_small'

-------------

`preprocess()` : Créé un `DatasetItem` et appelle `DatasetItem.loadFromFile()` pour chaque image dans le dossier.

-------------

**Exemple :**

    Classes[] = [a b c d]

    DatasetItem[] = [a b b c d d]

    samples =     [ [0 2 0 3]   // a
                    [2 1 0 4]   // b
                    [1 1 0 3]   // b
                    [2 3 4 0]   // c
                    [0 1 0 4]   // d
                    [1 0 1 4] ] // d

    responses =   [ [1 0 0 0]   // a
                    [0 1 0 0]   // b
                    [0 1 0 0]   // b
                    [0 0 1 0]   // c
                    [0 0 0 1]   // d
                    [0 0 0 1] ] // d
-------------

##OCR

    class OCR
    {
        saveModel(filename)
        loadModel(filename, type, flags)
        trainModel(type, flags, trainRatio, maxPerClass, verbose)

        charFromImage() // Disponible après 'loadModel' ou 'trainModel'
        charFromFile() // Disponible après 'loadModel' ou 'trainModel'

        static generateFolderList(flags)
    }

Génère une liste de dossier et créé un Dataset à partir de cette liste.

`type` est le type de modèle de classification

`flags = LETTERS | DIGITS | SYMBOLS`

`trainRatio` est le ratio entre les échantillon de test et d'entraînement.

`maxPerClass` est le nombre maximum d'échantillons par classe.

-------------

##Models

    class AbstractModel
    {
        load()
        save()
        train()
        predict()
    }

    class ANN : AbstractModel
    {
        train(samples, responses)
        predict(samples)
    }

    class KNearest : AbstractModel
    {
        train(samples, responses)
        predict(samples)
    }

-------------

##Analyse

Exemple : `(1, 1, 2, **2**, 4, 6, 9)`

- Moyenne : `3.6`

- Médiane : `2`

  Ecarts absolu (par rapport à la médiane) : `(1, 1, 0, 0, 2, 4, 7)`

 Triés : `(0, 0, 1, **1**, 2, 4, 7)`

- Ecart médian absolu = `1`

 La moitié des valeurs a un écart de moins de `1` avec la médiane et l'autre moitié a un écart de plus de `1` avec la médiane

- Coefficient de variation = `écart type / moyenne`

  Permet de comparer des écart type indépendamment du nombre d'éléments
