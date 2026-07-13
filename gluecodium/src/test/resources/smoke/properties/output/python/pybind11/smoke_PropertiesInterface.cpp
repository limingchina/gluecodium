

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/PropertiesInterface.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using PropertiesInterface = ::gluecodium::smoke::PropertiesInterface;

class PropertiesInterfaceTrampoline : public PropertiesInterface {
public:
    using PropertiesInterface::PropertiesInterface;

    ::smoke::PropertiesInterface::ExampleStruct& get_struct_property() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::smoke::PropertiesInterface::ExampleStruct&, PropertiesInterface, get_struct_property);
    }
    void set_struct_property(const ::smoke::PropertiesInterface::ExampleStruct& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, PropertiesInterface, set_struct_property, value);
    }
};

void register_PropertiesInterface(py::module_& module) {
    py::class_<PropertiesInterface, std::shared_ptr<PropertiesInterface>, PropertiesInterfaceTrampoline>(module, "PropertiesInterface")
        .def(py::init<>())
        .def_property("struct_property", py::overload_cast<>(&PropertiesInterface::get_struct_property, py::const_), py::overload_cast<const ::smoke::PropertiesInterface::ExampleStruct&>(&PropertiesInterface::set_struct_property))
        ;
}

