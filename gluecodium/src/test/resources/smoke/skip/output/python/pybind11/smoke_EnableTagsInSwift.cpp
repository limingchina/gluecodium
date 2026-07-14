

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/EnableTagsInSwift.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using EnableTagsInSwift = ::smoke::EnableTagsInSwift;

class EnableTagsInSwiftTrampoline : public EnableTagsInSwift {
public:
    using EnableTagsInSwift::EnableTagsInSwift;

    void enable_tagged(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, EnableTagsInSwift, enable_tagged);
    }
    void dont_enable_tagged(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, EnableTagsInSwift, dont_enable_tagged);
    }
    void enable_tagged_list(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, EnableTagsInSwift, enable_tagged_list);
    }
};

void register_EnableTagsInSwift(py::module_& module) {
    py::class_<EnableTagsInSwift, std::shared_ptr<EnableTagsInSwift>, EnableTagsInSwiftTrampoline>(module, "EnableTagsInSwift")
        .def(py::init<>())
        .def("enable_tagged", [](EnableTagsInSwift& self) {
            return self.enable_tagged();
        })
        .def("dont_enable_tagged", [](EnableTagsInSwift& self) {
            return self.dont_enable_tagged();
        })
        .def("enable_tagged_list", [](EnableTagsInSwift& self) {
            return self.enable_tagged_list();
        })
        ;
}

