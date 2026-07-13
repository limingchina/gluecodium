

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SkipTagsInSwift.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SkipTagsInSwift = ::gluecodium::smoke::SkipTagsInSwift;

class SkipTagsInSwiftTrampoline : public SkipTagsInSwift {
public:
    using SkipTagsInSwift::SkipTagsInSwift;

    void skip_tagged(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, SkipTagsInSwift, skip_tagged);
    }
    void dont_skip_tagged(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, SkipTagsInSwift, dont_skip_tagged);
    }
    void skip_tagged_list(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, SkipTagsInSwift, skip_tagged_list);
    }
};

void register_SkipTagsInSwift(py::module_& module) {
    py::class_<SkipTagsInSwift, std::shared_ptr<SkipTagsInSwift>, SkipTagsInSwiftTrampoline>(module, "SkipTagsInSwift")
        .def(py::init<>())
        .def("skip_tagged", &SkipTagsInSwift::skip_tagged)
        .def("dont_skip_tagged", &SkipTagsInSwift::dont_skip_tagged)
        .def("skip_tagged_list", &SkipTagsInSwift::skip_tagged_list)
        ;
}

