// This definition is needed for future-proofing your code
// see https://docs.python.org/3/c-api/arg.html#:~:text=Note%20For%20all,always%20define%20PY_SSIZE_T_CLEAN.
#define PY_SSIZE_T_CLEAN
// The actual Python API
#include <Python.h>
#include <vector>

struct letter_info {
    long occurance;
    long or_more;
    char letter;
    int locations_len;
    int locations[5];
    int not_locations_len;
    int not_locations[5];
};

bool match(letter_info &li, const char *str)
{
    int count = 0;
    for (int i=0; i<5; i++)
    {
        if (str[i] == li.letter )
        {
            count += 1;
        }
    }

    if ( li.or_more == 1 && count < li.occurance )
    {
        return false;
    }   
    if ( li.or_more == 0 && count != li.occurance )
    {
        return false;
    }   

    for (int i=0; i<li.locations_len; i++)
    {
        if ( str[li.locations[i]] != li.letter )
        {
            return false;
        } 
    }

    for (int i=0; i<li.not_locations_len; i++)
    {
        if ( str[li.not_locations[i]] == li.letter )
        {
            return false;
        } 
    }

    return true;
}

void fill_letter_info(PyObject* li_obj, letter_info& li)
{
    PyObject *attr = PyObject_GetAttrString(li_obj, "occurance");
    li.occurance = PyLong_AsLong(attr);
    Py_DECREF(attr);

    attr = PyObject_GetAttrString(li_obj, "or_more");
    li.or_more = PyLong_AsLong(attr);
    Py_DECREF(attr);

    attr = PyObject_GetAttrString(li_obj, "letter");
    li.letter = PyUnicode_AsUTF8(attr)[0];
    Py_DECREF(attr);

    attr = PyObject_GetAttrString(li_obj, "locations");
    li.locations_len = PyList_Size(attr);

    for (int i=0; i<li.locations_len && i<5; i++)
    {
        PyObject *loc = PyList_GetItem(attr, i);
        li.locations[i] = PyLong_AsLong(loc);
    }   
    Py_DECREF(attr);

    attr = PyObject_GetAttrString(li_obj, "not_locations");
    li.not_locations_len = PyList_Size(attr);

    for (int i=0; i<li.not_locations_len && i<5; i++)
    {
        PyObject *loc = PyList_GetItem(attr, i);
        li.not_locations[i] = PyLong_AsLong(loc);
    }   
    Py_DECREF(attr);
}

PyObject* c_match(PyObject* self, PyObject* args)
{
    const char *str;
    PyObject *li_obj;
    letter_info li;

    //printf("calling match\n");
    PyArg_ParseTuple(args, "Os", &li_obj, &str);
    fill_letter_info(li_obj, li);

    if ( match(li, str) )
    {
        Py_RETURN_TRUE;
    }
    else
    {
        Py_RETURN_FALSE;
    }
}

PyObject* c_filter(PyObject* self, PyObject* args)
{
    PyObject *words, *known_letters;
    std::vector<letter_info> li;
    Py_ssize_t pos = 0;
    PyObject *loc;
    PyObject *new_words = PyList_New(0);

    PyArg_ParseTuple(args, "OO", &words, &known_letters);
    li.resize(PyDict_Size(known_letters));
    int i = 0;

    while (PyDict_Next(known_letters, &pos, NULL, &loc)) 
    {
        fill_letter_info(loc, li[i]);
        i += 1;
    }

    //printf("got %lu known letters\n", li.size());
    for (int i=0; i<PyList_Size(words); i++)
    {
        PyObject *word_obj = PyList_GetItem(words, i);
        const char *word = PyUnicode_AsUTF8(word_obj);
        //printf("got word %s\n", word);
        bool copy = true;
        for (uint32_t j=0; j<li.size(); j++)
        {
            if ( match(li[j], word) == false )
            {
                copy = false;
                break;
            }
        }
        if ( copy )
        {
            //printf("%s - copy word \n", word);
            PyObject *word_obj = PyUnicode_FromString(word);
            PyList_Append(new_words, word_obj);
            Py_DECREF(word_obj);
        }
    }   

    return new_words;
}

// array containing the module's methods' definitions
// put here the methods to export
// the array must end with a {NULL} struct
PyMethodDef module_methods[] = 
{
    {"c_match", c_match, METH_VARARGS, "Method description"},
    {"c_filter", c_filter, METH_VARARGS, "Method description"},
    {NULL} // this struct signals the end of the array
};

// struct representing the module
struct PyModuleDef c_module =
{
    PyModuleDef_HEAD_INIT, // Always initialize this member to PyModuleDef_HEAD_INIT
    "wordle_fast", // module name
    "Module description", // module description
    -1, // module size (more on this later)
    module_methods // methods associated with the module
};

PyMODINIT_FUNC
PyInit_wordle_fast(void)
{
    return PyModule_Create(&c_module);
}
