# ngram
A tool to build language model by N-gram 

## use it as a program
``` shell
    ngram.py [--train|-t] <output>
        read document from stdin and train the data.
    ngram.py [--predict|-p] <model>
        read prefix from stdin, then return the best term list.
```

## use is as a library

* train
```
    lm = NGramTraining(gram=2) # bigram.
    for term in text:
        lm.add(term)
    lm.save(output_model)
```

* load model and predict:
``` python
    mod = NGramModel()
    mod.load(filename)
    print mod.predict(prefix)
```

## current works and todo

* need to add some smooth methods.
 * Addictive method / Lidstone method.
 * Jelinek-Mercer method.
 * Knecer-Ney Method.
* some matrics need to be add.
 * information entropy on a document prediction.
* test benchmark.




