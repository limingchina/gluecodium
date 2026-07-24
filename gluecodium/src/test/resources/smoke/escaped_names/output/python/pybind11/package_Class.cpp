

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/VectorHash.h"
#include "package/Class.h"
#include "package/Types.h"
#include "memory"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Class = ::package::Class;

class ClassTrampoline : public Class {
public:
    using Class::Class;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<Class> m_impl;

    using fun_return_type = ::gluecodium::Return< ::package::Types::Struct, ::std::error_code >;
    ::gluecodium::Return< ::package::Types::Struct, ::std::error_code > fun(
            const ::std::vector< ::package::Types::Struct >& double ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->fun(double);
        }
        PYBIND11_OVERRIDE_PURE(fun_return_type, Class, fun, double);
    }
    ::package::Types::Enum get_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_property();
        }
        PYBIND11_OVERRIDE_PURE(::package::Types::Enum, Class, get_property);
    }
    void set_property(const ::package::Types::Enum value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_property(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, Class, set_property, value);
    }
};

void register_package_Class(py::module_& module) {
    py::class_<Class, ::package::Interface, std::shared_ptr<Class>, ClassTrampoline>(module, "Class")
        // Adoption constructor: adopt an existing native instance returned by a factory into
        // the trampoline subclass and stash it in `m_impl` so virtual calls forward to the
        // real implementation instead of the pure-virtual stub. `init_alias` cannot be used
        // here because the returned instance is a foreign (non-trampoline) implementation;
        // instead we build a fresh trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<Class> native) {
            auto self = std::make_shared<ClassTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def(py::init<>())

        .def_static("constructor", &Class::constructor)
        .def_property("property", py::overload_cast<>(&Class::get_property, py::const_), py::overload_cast<const ::package::Types::Enum>(&Class::set_property))
        ;
}

