

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ParentNarrowTwo.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ParentNarrowTwo = ::smoke::ParentNarrowTwo;

class ParentNarrowTwoTrampoline : public ParentNarrowTwo {
public:
    using ParentNarrowTwo::ParentNarrowTwo;

    void parent_function_two(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, ParentNarrowTwo, parent_function_two);
    }
    ::std::string& get_parent_property_two() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::string&, ParentNarrowTwo, get_parent_property_two);
    }
    void set_parent_property_two(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ParentNarrowTwo, set_parent_property_two, value);
    }
};

void register_ParentNarrowTwo(py::module_& module) {
    py::class_<ParentNarrowTwo, std::shared_ptr<ParentNarrowTwo>, ParentNarrowTwoTrampoline>(module, "ParentNarrowTwo")
        .def(py::init<>())
        .def("parent_function_two", [](ParentNarrowTwo& self) {
            return self.parent_function_two();
        })
        .def_property("parent_property_two", py::overload_cast<>(&ParentNarrowTwo::get_parent_property_two, py::const_), py::overload_cast<const ::std::string&>(&ParentNarrowTwo::set_parent_property_two))
        ;
}

