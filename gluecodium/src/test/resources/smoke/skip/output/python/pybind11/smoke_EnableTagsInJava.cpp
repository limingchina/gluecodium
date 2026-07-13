

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/EnableTagsInJava.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using EnableTagsInJava = ::gluecodium::smoke::EnableTagsInJava;

class EnableTagsInJavaTrampoline : public EnableTagsInJava {
public:
    using EnableTagsInJava::EnableTagsInJava;

    void enable_tagged(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, EnableTagsInJava, enable_tagged);
    }
    void dont_enable_tagged(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, EnableTagsInJava, dont_enable_tagged);
    }
    void enable_tagged_list(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, EnableTagsInJava, enable_tagged_list);
    }
};

void register_EnableTagsInJava(py::module_& module) {
    py::class_<EnableTagsInJava, std::shared_ptr<EnableTagsInJava>, EnableTagsInJavaTrampoline>(module, "EnableTagsInJava")
        .def(py::init<>())
        .def("enable_tagged", &EnableTagsInJava::enable_tagged)
        .def("dont_enable_tagged", &EnableTagsInJava::dont_enable_tagged)
        .def("enable_tagged_list", &EnableTagsInJava::enable_tagged_list)
        ;
}

