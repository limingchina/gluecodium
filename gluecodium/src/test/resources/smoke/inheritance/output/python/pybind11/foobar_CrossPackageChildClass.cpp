

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
#include "foobar/CrossPackageChildClass.h"
#include "smoke/ParentInterface.h"
#include "string"

using CrossPackageChildClass = ::foobar::CrossPackageChildClass;

class CrossPackageChildClassTrampoline : public CrossPackageChildClass {
public:
    using CrossPackageChildClass::CrossPackageChildClass;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<CrossPackageChildClass> m_impl;

    void root_method(
            /* no args */ ) override {
        if (m_impl) {
            m_impl->root_method();
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const CrossPackageChildClass*>(this), "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e726f6f744d6574686f64")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, CrossPackageChildClass, "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e726f6f744d6574686f64", root_method);
        }
        PYBIND11_OVERRIDE_PURE(void, CrossPackageChildClass, root_method);
    }
    ::std::string get_root_property() const override {
        if (m_impl) {
            return m_impl->get_root_property();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const CrossPackageChildClass*>(this), "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e726f6f7450726f7065727479_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::string, CrossPackageChildClass, "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e726f6f7450726f7065727479_get", get_root_property);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, CrossPackageChildClass, get_root_property);
    }
    void set_root_property(const ::std::string& value) override {
        if (m_impl) {
            m_impl->set_root_property(value);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const CrossPackageChildClass*>(this), "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e726f6f7450726f7065727479_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, CrossPackageChildClass, "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e726f6f7450726f7065727479_set", set_root_property, value);
        }
        PYBIND11_OVERRIDE_PURE(void, CrossPackageChildClass, set_root_property, value);
    }
};



void register_foobar_CrossPackageChildClass(py::module_& module) {
auto cls_CrossPackageChildClass = py::class_<CrossPackageChildClass, ::smoke::ParentInterface, std::shared_ptr<CrossPackageChildClass>, CrossPackageChildClassTrampoline>(module, "foobar_CrossPackageChildClass")
        .def("__gluecodium_id__", [](const CrossPackageChildClass& self) {
            return gluecodium::python::native_identity(self);
        })
        .def_static("__gluecodium_downcast__", [](const py::object& native) -> py::object {
            try {
                auto base = native.cast<std::shared_ptr<::smoke::ParentInterface>>();
                auto derived = gluecodium::python::dynamic_pointer_cast<CrossPackageChildClass>(base);
                if (derived) return py::cast(derived);
            } catch (const py::cast_error&) {
            }
            return py::none();
        })
        // Adoption constructor: adopt an existing native instance returned by a factory into
        // the trampoline subclass and stash it in `m_impl` so virtual calls forward to the
        // real implementation instead of the pure-virtual stub. `init_alias` cannot be used
        // here because the returned instance is a foreign (non-trampoline) implementation;
        // instead we build a fresh trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<CrossPackageChildClass> native) {
            auto self = std::make_shared<CrossPackageChildClassTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("root_method", [](CrossPackageChildClass& self) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.root_method(); });
        })
        .def_property("root_property", [](const CrossPackageChildClass& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_root_property();
            });
        }, [](CrossPackageChildClass& self, const ::std::string& value) {
            gluecodium::python::call_native([&] {
                self.set_root_property(value);
            });
        })
        ;


}
