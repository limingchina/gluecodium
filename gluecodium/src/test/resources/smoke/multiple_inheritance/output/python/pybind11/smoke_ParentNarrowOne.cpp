

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ParentNarrowOne.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ParentNarrowOne = ::gluecodium::smoke::ParentNarrowOne;

class ParentNarrowOneTrampoline : public ParentNarrowOne {
public:
    using ParentNarrowOne::ParentNarrowOne;

    void parent_function_one(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ParentNarrowOne, parent_function_one);
    }
    ::std::string& get_parent_property_one() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::string&, ParentNarrowOne, get_parent_property_one);
    }
    void set_parent_property_one(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ParentNarrowOne, set_parent_property_one, value);
    }
};

void register_ParentNarrowOne(py::module_& module) {
    py::class_<ParentNarrowOne, std::shared_ptr<ParentNarrowOne>, ParentNarrowOneTrampoline>(module, "ParentNarrowOne")
        .def("parent_function_one", &ParentNarrowOne::parent_function_one)
        .def_property("parent_property_one", py::overload_cast<>(&ParentNarrowOne::get_parent_property_one, py::const_), py::overload_cast<const ::std::string&>(&ParentNarrowOne::set_parent_property_one))
        ;
}

