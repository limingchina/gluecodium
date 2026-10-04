

#include <Python.h>
#include <pybind11/pybind11.h>
#include "_opaque_types.h"
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "foo/Bar.h"
#include "cstdint"
#include "string"

using ExternalInterface = ::smoke::ExternalInterface;
using some_Struct = ::smoke::ExternalInterface::some_Struct;
using some_Enum = ::smoke::ExternalInterface::some_Enum;

class ExternalInterfaceTrampoline : public ExternalInterface {
public:
    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<ExternalInterface> m_impl;

    void some_Method(
            const int8_t some_parameter ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->some_Method(some_parameter);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ExternalInterface, some_method, some_parameter);
    }
    ::std::string get_Me() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_Me();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, ExternalInterface, get_Me);
    }
};



void register_smoke_ExternalInterface(py::module_& module) {
auto cls_ExternalInterface = py::class_<ExternalInterface>(module, "smoke_ExternalInterface");

auto cls_ExternalInterfacesome_Struct = py::class_<some_Struct>(cls_ExternalInterface, "SomeStruct")
        .def_readwrite("some_field", &some_Struct::some_Field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("some_field"))
        ;

auto cls_ExternalInterfacesome_Enum = py::enum_<some_Enum>(cls_ExternalInterface, "SomeEnum")
        .value("SOME_VALUE", some_Enum::some_Value)
        ;


}
