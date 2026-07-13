

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SkipTagsInKotlin.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SkipTagsInKotlin = ::gluecodium::smoke::SkipTagsInKotlin;

class SkipTagsInKotlinTrampoline : public SkipTagsInKotlin {
public:
    using SkipTagsInKotlin::SkipTagsInKotlin;

    void skip_tagged(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, SkipTagsInKotlin, skip_tagged);
    }
    void dont_skip_tagged(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, SkipTagsInKotlin, dont_skip_tagged);
    }
    void skip_tagged_list(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, SkipTagsInKotlin, skip_tagged_list);
    }
};

void register_SkipTagsInKotlin(py::module_& module) {
    py::class_<SkipTagsInKotlin, std::shared_ptr<SkipTagsInKotlin>, SkipTagsInKotlinTrampoline>(module, "SkipTagsInKotlin")
        .def("skip_tagged", &SkipTagsInKotlin::skip_tagged)
        .def("dont_skip_tagged", &SkipTagsInKotlin::dont_skip_tagged)
        .def("skip_tagged_list", &SkipTagsInKotlin::skip_tagged_list)
        ;
}

