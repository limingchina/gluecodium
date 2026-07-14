

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SkipTagsInDart.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SkipTagsInDart = ::smoke::SkipTagsInDart;

class SkipTagsInDartTrampoline : public SkipTagsInDart {
public:
    using SkipTagsInDart::SkipTagsInDart;

    void skip_tagged(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, SkipTagsInDart, skip_tagged);
    }
    void dont_skip_tagged(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, SkipTagsInDart, dont_skip_tagged);
    }
    void skip_tagged_list(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, SkipTagsInDart, skip_tagged_list);
    }
};

void register_SkipTagsInDart(py::module_& module) {
    py::class_<SkipTagsInDart, std::shared_ptr<SkipTagsInDart>, SkipTagsInDartTrampoline>(module, "SkipTagsInDart")
        .def(py::init<>())
        .def("skip_tagged", [](SkipTagsInDart& self) {
            return self.skip_tagged();
        })
        .def("dont_skip_tagged", [](SkipTagsInDart& self) {
            return self.dont_skip_tagged();
        })
        .def("skip_tagged_list", [](SkipTagsInDart& self) {
            return self.skip_tagged_list();
        })
        ;
}

