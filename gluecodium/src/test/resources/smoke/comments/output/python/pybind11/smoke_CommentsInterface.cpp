

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/CommentsInterface.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using CommentsInterface = ::smoke::CommentsInterface;

class CommentsInterfaceTrampoline : public CommentsInterface {
public:
    using CommentsInterface::CommentsInterface;

    bool some_method_with_all_comments(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(bool, CommentsInterface, some_method_with_all_comments, input);
    }
    bool some_method_with_input_comments(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(bool, CommentsInterface, some_method_with_input_comments, input);
    }
    bool some_method_with_output_comments(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(bool, CommentsInterface, some_method_with_output_comments, input);
    }
    bool some_method_with_no_comments(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(bool, CommentsInterface, some_method_with_no_comments, input);
    }
    void some_method_without_return_type_with_all_comments(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, CommentsInterface, some_method_without_return_type_with_all_comments, input);
    }
    void some_method_without_return_type_with_no_comments(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, CommentsInterface, some_method_without_return_type_with_no_comments, input);
    }
    bool some_method_without_input_parameters_with_all_comments(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(bool, CommentsInterface, some_method_without_input_parameters_with_all_comments);
    }
    bool some_method_without_input_parameters_with_no_comments(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(bool, CommentsInterface, some_method_without_input_parameters_with_no_comments);
    }
    void some_method_with_nothing(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, CommentsInterface, some_method_with_nothing);
    }
    void some_method_without_return_type_or_input_parameters(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, CommentsInterface, some_method_without_return_type_or_input_parameters);
    }
    bool is_some_property() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(bool, CommentsInterface, is_some_property);
    }
    void set_some_property(const bool value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, CommentsInterface, set_some_property, value);
    }
};

void register_CommentsInterface(py::module_& module) {
    py::class_<CommentsInterface, std::shared_ptr<CommentsInterface>, CommentsInterfaceTrampoline>(module, "CommentsInterface")
        .def(py::init<>())
        .def("some_method_with_all_comments", &CommentsInterface::some_method_with_all_comments, py::arg("input"))
        .def("some_method_with_input_comments", &CommentsInterface::some_method_with_input_comments, py::arg("input"))
        .def("some_method_with_output_comments", &CommentsInterface::some_method_with_output_comments, py::arg("input"))
        .def("some_method_with_no_comments", &CommentsInterface::some_method_with_no_comments, py::arg("input"))
        .def("some_method_without_return_type_with_all_comments", &CommentsInterface::some_method_without_return_type_with_all_comments, py::arg("input"))
        .def("some_method_without_return_type_with_no_comments", &CommentsInterface::some_method_without_return_type_with_no_comments, py::arg("input"))
        .def("some_method_without_input_parameters_with_all_comments", &CommentsInterface::some_method_without_input_parameters_with_all_comments)
        .def("some_method_without_input_parameters_with_no_comments", &CommentsInterface::some_method_without_input_parameters_with_no_comments)
        .def("some_method_with_nothing", &CommentsInterface::some_method_with_nothing)
        .def("some_method_without_return_type_or_input_parameters", &CommentsInterface::some_method_without_return_type_or_input_parameters)
        .def_property("is_some_property", py::overload_cast<>(&CommentsInterface::is_some_property, py::const_), py::overload_cast<const bool>(&CommentsInterface::set_some_property))
        ;
}

