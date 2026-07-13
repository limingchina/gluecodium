

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/DeprecationCommentsOnly.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DeprecationCommentsOnly = ::gluecodium::smoke::DeprecationCommentsOnly;

class DeprecationCommentsOnlyTrampoline : public DeprecationCommentsOnly {
public:
    using DeprecationCommentsOnly::DeprecationCommentsOnly;

    bool some_method_with_all_comments(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(bool, DeprecationCommentsOnly, some_method_with_all_comments, input);
    }
    bool is_some_property() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(bool, DeprecationCommentsOnly, is_some_property);
    }
    void set_some_property(const bool value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, DeprecationCommentsOnly, set_some_property, value);
    }
};

void register_DeprecationCommentsOnly(py::module_& module) {
    py::class_<DeprecationCommentsOnly, std::shared_ptr<DeprecationCommentsOnly>, DeprecationCommentsOnlyTrampoline>(module, "DeprecationCommentsOnly")
        .def(py::init<>())
        .def("some_method_with_all_comments", &DeprecationCommentsOnly::some_method_with_all_comments, py::arg("input"))
        .def_property("is_some_property", py::overload_cast<>(&DeprecationCommentsOnly::is_some_property, py::const_), py::overload_cast<const bool>(&DeprecationCommentsOnly::set_some_property))
        ;
}

