

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/Locale.h"
#include "gluecodium/TimePointHash.h"
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/OuterStruct.h"
#include "chrono"
#include "cstdint"
#include "functional"
#include "memory"
#include "string"
#include "unordered_map"
#include "unordered_set"
#include "vector"

using OuterStruct = ::smoke::OuterStruct;
using InnerStruct = ::smoke::OuterStruct::InnerStruct;
using InnerClass = ::smoke::OuterStruct::InnerClass;
using Builder = ::smoke::OuterStruct::Builder;
using InnerInterface = ::smoke::OuterStruct::InnerInterface;
using InnerEnum = ::smoke::OuterStruct::InnerEnum;

class InnerInterfaceTrampoline : public InnerInterface {
public:
    using InnerInterface::InnerInterface;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<InnerInterface> m_impl;

    using bar_baz_return_type = ::std::unordered_map< ::std::string, ::std::shared_ptr< ::std::vector< uint8_t > > >;
    ::std::unordered_map< ::std::string, ::std::shared_ptr< ::std::vector< uint8_t > > > bar_baz(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->bar_baz();
        }
        PYBIND11_OVERRIDE_PURE(bar_baz_return_type, InnerInterface, bar_baz);
    }
};



void register_smoke_OuterStruct(py::module_& module) {
auto cls_OuterStruct = py::class_<OuterStruct>(module, "smoke_OuterStruct")
        .def_readwrite("field", &OuterStruct::field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("field"))
        .def("do_nothing", &OuterStruct::do_nothing)
        ;

auto cls_OuterStructInnerStruct = py::class_<InnerStruct>(cls_OuterStruct, "InnerStruct")
        .def_readwrite("other_field", &InnerStruct::other_field)
        .def(py::init<>())
        .def(py::init<::std::vector< ::std::chrono::system_clock::time_point >>(), py::arg("other_field"))
        .def("do_something", &InnerStruct::do_something)
        ;

auto cls_OuterStructInnerClass = py::class_<InnerClass, std::shared_ptr<InnerClass>>(cls_OuterStruct, "InnerClass")
        .def("__gluecodium_id__", [](const InnerClass& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
                .def("foo_bar", [](InnerClass& self) -> py::object {
                        return gluecodium::python::to_python_regular(self.foo_bar());
                })
        ;

auto cls_OuterStructBuilder = py::class_<Builder, std::shared_ptr<Builder>>(cls_OuterStruct, "Builder")
        .def("__gluecodium_id__", [](const Builder& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("create", &Builder::create)
        .def("field", &Builder::field, py::arg("value"))
        .def("build", &Builder::build)
        ;

auto cls_OuterStructInnerInterface = py::class_<InnerInterface, std::shared_ptr<InnerInterface>, InnerInterfaceTrampoline>(cls_OuterStruct, "InnerInterface")
        .def("__gluecodium_id__", [](const InnerInterface& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<InnerInterface> native) {
            auto self = std::make_shared<InnerInterfaceTrampoline>();
            self->m_impl = native;
            return self;
        }))
                .def("bar_baz", [](InnerInterface& self) -> py::object {
                        return gluecodium::python::to_python_regular(self.bar_baz());
                })
        ;

auto cls_OuterStructInnerEnum = py::enum_<InnerEnum>(cls_OuterStruct, "InnerEnum")
        .value("FOO", InnerEnum::FOO)
        .value("BAR", InnerEnum::BAR)
        ;

    static py::exception<::std::error_code> exc_InstantiationError(cls_OuterStruct, "InstantiationError");
    py::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p) std::rethrow_exception(p);
        } catch (const ::std::error_code& e) {
            PyErr_SetString(exc_InstantiationError.ptr(), e.message().c_str());
        }
    });
    pybind11::detail::registerReturnError<::std::error_code>(exc_InstantiationError.ptr());


}
