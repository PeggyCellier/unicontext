# UniContext

## Introduction

Contexts are used in most SmartFCA algorithms. They are defined in FCA theory by a set of objects, a set of attributes, and an incidence relationship between the set of objects and the set of attributes. Today, this definition has been extended to an incidence relationship between objects and themselves. This definition is mainly used by the relational extensions of FCA, e.g. Graph-FCA and RCA.

A formal context $K := (O,A,I)$ consists of a set of objects O (a category), a set of attributes A and an incidence relation I between $O$ and $A$. A relational context $R := (O_1,.. , O_n, I)$ consists of a family of categories $O_1$,.. , $O_n$ and a incidence relation $I \subset O_1 \times .. \times O_n$.

In a UniContext, sets of objects depending of a formal or relational context are defined at the root of the JSON object, under the $categories$ field. Categories may or may not be common to multiples formal or relational contexts. Attributes depending of a formal context are defined within the formal context. Incidence relation depending of a formal or relational context are defined within the formal or relational context.

## Definition

The atomic types used in the context definition are defined in the table below.

| definition | type |
|---|---|
|$ContextName$|string|
|$ContextDescription$|string|
|$CategoryId$|string|
|$FormalContextId$|string|
|$RelationalContextId$|string|
|$obj_i$|string|
|$attribute_i$|string|

An UniContext file is a file containing a JSON object with a defined list of key-value pair. Values can be themselves JSON objects or of atomic types.

    <ContextObj> ::= {
        name : <ContextName>
        description : <ContextDescription>, (optionnal)
        categories : { <CategoryId> : <categoryObj>, ..},
        formalContexts : { 
            <FormalContextId> : <formalContextObj>, 
            ... 
        },
        relationalContexts : { 
            <RelationalContextId> : <relationalContextObj>, 
            ...
        }
    }

The $ContextObj$ is the root object of a UniContext. It contains its name, its optional description, the list of its categories indexed by the category name, the list of its formal contexts indexed by the formal context name, and the list of its relational context indexed by the relational context name.

    <categoryObj> ::= [obj_1, obj_2,...]

    <formalContextObj> ::= {
        domain : <CategoryId>,
        attributes : [attribute_1, attribute_2, ...],
        incidence : { 
            obj_1 : <incidence_1>, 
            obj_2 : <incidence_2>,
            ...
        }
    }

    <relationalContextObj> ::= {
        domain : <CategoryId>,
        range : <CategoryId>,
        incidence : { 
            obj_1 : <incidenceObj_1>,
            obj_2 : <incidenceObj_2>,
            ...
        }
    }
    | {
        domain : <CategoryId>,
        range : [<CategoryId_1>, <CategoryId_2>, ...],
        incidence : {
            obj_1 : <incidenceMultiObj_1>,
            obj_2 : <incidenceMultiObj_2>
        }
    }


    <incidence_i> ::= [attr_1, attr_2,...] 

    <incidenceObj_i> ::= [obj_1, obj_2,...] 

    <incidenceMultiObj_i> ::= [[obj^1_1, obj^1_2,...], [obj^2_1, obj^2_2,...], ...] 

A $relationalContextObj$ defines an n-ary relational context $R := (O_1,..,O_n,I)$. If $n = 2$, then the $domain$ of the context is the category $O_1$ and the $range$ of the context is the category $O_2$. If $n \geq 3$, then the $domain$ of the context is $O_1$ and the $range$ of the domain is the list $[O_2,... ,O_n]$.

The incidence relation $I$ of a $relationalContextObj$ of arity n is defined as\\ followed :

- if $n=2$, the incidence relation is the dictionary indexed by value $obj_1 \in O_1$ of the domain of $I$ and valued by the list of every $obj^i_2$ such as $(obj_1, obj^i_2) \in I$
- if $n \geq 3$, the incidence relation is the dictionary indexed by value $obj_1 \in O_1$ of the domain of $I$ and valued by the list of list $[obj^i_2,.. ,obj^i_n]$ such as $(obj^i_1, obj^i_2 .., obj^i_n) \in I$

## Examples

### British Royal Family

Here is an UniContext describing the British royal family. The context consists of (1-) a category $person$, which is the set of members of the royal family, (2-) an incidence relation $Person$ between the category $person$ and the set of attributes $\{"male", "female", "child", "adult", "alive"\}$ forming a formal context, and (3-) an incidence relation $parent$ between the category $person$ and itself, forming a relational context. 

    {
        "name" : "British royal family",
        "categories" : {
            "person" : ["Charles", "William", "Harry", "Georges", "Diana", "Kate", 
    "Charlotte"]
        },
        "formalContexts" : {
            "Person" : {
                "domain" : "person",
                "attributes" : ["male", "female", "child", "adult", "alive"],
                "incidence": {
                    "Charles" : ["male", "adult", "alive"],
                    "William" : ["male", "adult", "alive"],
                    "Harry" : ["male", "adult", "alive"],
                    "Georges" : ["male", "child", "alive"],
                    "Diana": ["female", "adult"],
                    "Kate": ["female", "adult", "alive"],
                    "Charlotte": ["female", "child", "alive"]
                }
            }
        },
        "relationalContexts" : {
            "parent" : {
                "domain" : "person",
                "range": "person",
                "incidence": {
                    "William" : ["Charles", "Diana"],
                    "Harry" : ["Charles", "Diana"],
                    "Georges" : ["William", "Kate"],
                    "Charlotte": ["William", "Kate"]
                }
            }
        }
    }

### Car insurances

Here is an UniContext describing owners with their cars and the insurances they subscribed. There are three categories, $person$, $car$, and $insurance$, and a relational context that describes which insurance the owner has subscribed to for his car. Note that the relational context is a ternary relation, and thus the range of the context is the list of two categories $car$ and $insurance$. The incidence relation is indexed by the owner of the car and the values are the list of list of instances of $car$ and $insurance$.

    {
        "name" : "Car insurances",
        "categories" : {
            "person" : ["Alice", "Bob", "Charles", "Brian"],
            "car": ["Clio", "Golf", "Corolla", "Civic", "Fiesta", "Corsa"],
            "insurance": ["liability", "collision", "comprehensive", "PIP"]
        },
        "formalContexts" : {},
        "relationalContexts" : {
            "hasInsuranceForCar" : {
                "domain" : "person",
                "range": ["car", "insurance" ],
                "incidence": {
                    "Alice" : [["Corolla", "liability"]],
                    "Bob" : [["Fiesta", "collision"], ["Corsa", "PIP"]],
                    "Charles" : [["Golf", "comprehensive"], ["Civic", "liability"]],
                    "Brian": [["Clio", "collision"]]
                }
            }
        }
    }

### Researchers

Here is an UniContext describing Researchers, their job, who they have worked with, in which city they worked on which paper, and the fields of each paper.


    {
        "name": "Researchers",
        "categories" : {
            "person": ["Nicolas", "Marine", "Pierre", "Tom"],
            "places": ["Bordeaux", "Lille", "Strasbourg", "Rennes"],
            "papers": ["paperA", "paperB", "paperC", "paperD"]
        },
        "formalContexts" : {
            "employment" : {
                "domain" : "person",
                "attributes" : ["Phd", "teacher", "researcher", "engineer"],
                "incidence" : {
                    "Nicolas" : ["engineer"],
                    "Marine" : ["teacher"],
                    "Pierre" : ["researcher", "teacher", "Phd"],
                    "Tom" : ["researcher", "Phd"]
                }
            }, 
            "field" : {
                "domain" : "paper",
                "attributes" : ["Machine Learning", "Data Mining", "Linguistics", "Biology"],
                "incidence" : {
                    "paperA" : ["Machine Learning", "Linguistics"],
                    "paperB" : ["Data Mining", "Biology"],
                    "paperC" : ["Machine Learning", "Biology"],
                    "paperD" : ["Linguistics"]
                }
            }
        },
        "relationalContexts" : {
            "hasWorkedWith" : {
                "domain" : "person",
                "range" : "person",
                "incidence" : {
                    "Nicolas" : ["Marine"],
                    "Marine" : ["Nicolas", "Pierre"],
                    "Pierre": ["Marine", "Tom"],
                    "Tom": ["Pierre"]
                }
            },
            "hasWorkedInOn" : {
                "domain" : "person",
                "range" : ["place", "paper"],
                "incidence" : {
                    "Nicolas" : [["Bordeaux", "paperA"]],
                    "Marine" : [["Bordeaux", "paperA"], ["Lille", "paperB"]],
                    "Pierre": [["Lille", "paperB"], ["Rennes", "paperC"]],
                    "Tom" : [["Rennes", "paperC"], ["Strasbourg", "paperD"]]
                }
            }
        }
    }

## Install

the scripts need python 3 and the library pydantic to be executed

## Tests

### .cxt files

To convert a .cxt file to the Unicontext format, use the command line, as an example :

    python converters/cxt2uni.py data/liveinwater.cxt

To convert a Unicontext file to the .cxt format, use the command line, as an example :

    python converters/uni2cxt.py data/liveinwater.json

### .rcft files

To convert a .rcft file to the Unicontext format, use the command line, as an example :

    python converters/rcft2uni.py data/social_relation.rcft

To convert a Unicontext file to the .rcft format, use the command line, as an example :

    python converters/uni2cxt.py data/social_relation.json

### .p files

#### well formated .p files

The converter p2uni accepts only a subset of the .p grammar. To be converted, the .p file needs :
- only have one rule
- the rule should have no head
- the patterns of the rules should have only one object as argument and the description block should be a list of comma separated values
- there should be only one pattern per line
- the ":-" and "." statement should be written on a single line with no other statement
- the objects should appear once in a pattern head


Examples of not well formatted .p file :

| file | reason |
| -----|--------|
| data/edge_cases_p/royal_ruleHead.p | the rule has head |
| data/edge_cases_p/royal_twoRules.p | there are two rules |
| data/edge_cases_p/royal_ampersand.p | ampersand in pattern details |

To convert a .p file to the Unicontext format, use the command line, as an example :

    python converters/p2uni.py data/royal.p

To convert a .p file to the Unicontext format while specifying the first relation of an object as its category, use the command line, as an example :

    python converters/p2uni.py -categories data/royal.p

To convert a Unicontext file to the .p format, use the command line, as an example :

    python converters/uni2p.py data/royal.json