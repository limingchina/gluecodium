

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/EnableTagsInKotlin.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using EnableTagsInKotlin = ::smoke::EnableTagsInKotlin;

class EnableTagsInKotlinTrampoline : public EnableTagsInKotlin {
public:
    using EnableTagsInKotlin::EnableTagsInKotlin;

    void enable_tagged(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, EnableTagsInKotlin, enable_tagged);
    }
    void dont_enable_tagged(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, EnableTagsInKotlin, dont_enable_tagged);
    }
    void enable_tagged_list(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, EnableTagsInKotlin, enable_tagged_list);
    }
};

void register_EnableTagsInKotlin(py::module_& module) {
    py::class_<EnableTagsInKotlin, std::shared_ptr<EnableTagsInKotlin>, EnableTagsInKotlinTrampoline>(module, "EnableTagsInKotlin")
        .def(py::init<>())
        .def("enable_tagged", [](EnableTagsInKotlin& self) {
            return self.enable_tagged();
        })
        .def("dont_enable_tagged", [](EnableTagsInKotlin& self) {
            return self.dont_enable_tagged();
        })
        .def("enable_tagged_list", [](EnableTagsInKotlin& self) {
            return self.enable_tagged_list();
        })
        ;
}

