

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/DeprecationComments.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DeprecationComments = ::smoke::DeprecationComments;

class DeprecationCommentsTrampoline : public DeprecationComments {
public:
    using DeprecationComments::DeprecationComments;

    bool some_method_with_all_comments(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(bool, DeprecationComments, some_method_with_all_comments, input);
    }
    bool is_some_property() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(bool, DeprecationComments, is_some_property);
    }
    void set_some_property(const bool value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, DeprecationComments, set_some_property, value);
    }
    ::std::string& get_property_but_not_accessors() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::string&, DeprecationComments, get_property_but_not_accessors);
    }
    void set_property_but_not_accessors(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, DeprecationComments, set_property_but_not_accessors, value);
    }
};

void register_DeprecationComments(py::module_& module) {
    py::class_<DeprecationComments, std::shared_ptr<DeprecationComments>, DeprecationCommentsTrampoline>(module, "DeprecationComments")
        .def(py::init<>())
        .def("some_method_with_all_comments", &DeprecationComments::some_method_with_all_comments, py::arg("input"))
        .def_property("is_some_property", py::overload_cast<>(&DeprecationComments::is_some_property, py::const_), py::overload_cast<const bool>(&DeprecationComments::set_some_property))
        .def_property("property_but_not_accessors", py::overload_cast<>(&DeprecationComments::get_property_but_not_accessors, py::const_), py::overload_cast<const ::std::string&>(&DeprecationComments::set_property_but_not_accessors))
        ;
}

