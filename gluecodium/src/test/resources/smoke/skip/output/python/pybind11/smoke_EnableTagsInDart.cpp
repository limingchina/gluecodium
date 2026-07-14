

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/EnableTagsInDart.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using EnableTagsInDart = ::smoke::EnableTagsInDart;

class EnableTagsInDartTrampoline : public EnableTagsInDart {
public:
    using EnableTagsInDart::EnableTagsInDart;

    void enable_tagged(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, EnableTagsInDart, enable_tagged);
    }
    void dont_enable_tagged(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, EnableTagsInDart, dont_enable_tagged);
    }
    void enable_tagged_list(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, EnableTagsInDart, enable_tagged_list);
    }
};

void register_EnableTagsInDart(py::module_& module) {
    py::class_<EnableTagsInDart, std::shared_ptr<EnableTagsInDart>, EnableTagsInDartTrampoline>(module, "EnableTagsInDart")
        .def(py::init<>())
        .def("enable_tagged", [](EnableTagsInDart& self) {
            return self.enable_tagged();
        })
        .def("dont_enable_tagged", [](EnableTagsInDart& self) {
            return self.dont_enable_tagged();
        })
        .def("enable_tagged_list", [](EnableTagsInDart& self) {
            return self.enable_tagged_list();
        })
        ;
}

