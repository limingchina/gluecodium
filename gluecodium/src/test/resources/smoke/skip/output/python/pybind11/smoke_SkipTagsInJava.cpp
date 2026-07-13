

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SkipTagsInJava.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SkipTagsInJava = ::gluecodium::smoke::SkipTagsInJava;

class SkipTagsInJavaTrampoline : public SkipTagsInJava {
public:
    using SkipTagsInJava::SkipTagsInJava;

    void skip_tagged(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, SkipTagsInJava, skip_tagged);
    }
    void dont_skip_tagged(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, SkipTagsInJava, dont_skip_tagged);
    }
    void skip_tagged_list(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, SkipTagsInJava, skip_tagged_list);
    }
};

void register_SkipTagsInJava(py::module_& module) {
    py::class_<SkipTagsInJava, std::shared_ptr<SkipTagsInJava>, SkipTagsInJavaTrampoline>(module, "SkipTagsInJava")
        .def(py::init<>())
        .def("skip_tagged", &SkipTagsInJava::skip_tagged)
        .def("dont_skip_tagged", &SkipTagsInJava::dont_skip_tagged)
        .def("skip_tagged_list", &SkipTagsInJava::skip_tagged_list)
        ;
}

