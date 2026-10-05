

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
#include "smoke/ChildClassFromClass.h"
#include "smoke/ChildWithParentClassReferences.h"
#include "smoke/ParentClass.h"
#include "smoke/ParentWithClassReferences.h"
#include "memory"

using ChildWithParentClassReferences = ::smoke::ChildWithParentClassReferences;

class ChildWithParentClassReferencesTrampoline : public ChildWithParentClassReferences {
public:
    using ChildWithParentClassReferences::ChildWithParentClassReferences;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<ChildWithParentClassReferences> m_impl;

    ::std::shared_ptr< ::smoke::ChildClassFromClass > class_function(
            /* no args */ ) override {
        if (m_impl) {
            return m_impl->class_function();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ChildWithParentClassReferences*>(this), "__gluecodium_callback_736d6f6b652e506172656e7457697468436c6173735265666572656e6365732e636c61737346756e6374696f6e")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::shared_ptr< ::smoke::ChildClassFromClass >, ChildWithParentClassReferences, "__gluecodium_callback_736d6f6b652e506172656e7457697468436c6173735265666572656e6365732e636c61737346756e6374696f6e", class_function);
        }
        PYBIND11_OVERRIDE_PURE(::std::shared_ptr< ::smoke::ChildClassFromClass >, ChildWithParentClassReferences, class_function);
    }
    ::std::shared_ptr< ::smoke::ParentClass > get_class_property() const override {
        if (m_impl) {
            return m_impl->get_class_property();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ChildWithParentClassReferences*>(this), "__gluecodium_callback_736d6f6b652e506172656e7457697468436c6173735265666572656e6365732e636c61737350726f7065727479_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::shared_ptr< ::smoke::ParentClass >, ChildWithParentClassReferences, "__gluecodium_callback_736d6f6b652e506172656e7457697468436c6173735265666572656e6365732e636c61737350726f7065727479_get", get_class_property);
        }
        PYBIND11_OVERRIDE_PURE(::std::shared_ptr< ::smoke::ParentClass >, ChildWithParentClassReferences, get_class_property);
    }
    void set_class_property(const ::std::shared_ptr< ::smoke::ParentClass >& value) override {
        if (m_impl) {
            m_impl->set_class_property(value);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ChildWithParentClassReferences*>(this), "__gluecodium_callback_736d6f6b652e506172656e7457697468436c6173735265666572656e6365732e636c61737350726f7065727479_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, ChildWithParentClassReferences, "__gluecodium_callback_736d6f6b652e506172656e7457697468436c6173735265666572656e6365732e636c61737350726f7065727479_set", set_class_property, value);
        }
        PYBIND11_OVERRIDE_PURE(void, ChildWithParentClassReferences, set_class_property, value);
    }
};



void register_smoke_ChildWithParentClassReferences(py::module_& module) {
auto cls_ChildWithParentClassReferences = py::class_<ChildWithParentClassReferences, ::smoke::ParentWithClassReferences, std::shared_ptr<ChildWithParentClassReferences>, ChildWithParentClassReferencesTrampoline>(module, "smoke_ChildWithParentClassReferences")
        .def("__gluecodium_id__", [](const ChildWithParentClassReferences& self) {
            return gluecodium::python::native_identity(self);
        })
        .def_static("__gluecodium_downcast__", [](const py::object& native) -> py::object {
            try {
                auto base = native.cast<std::shared_ptr<::smoke::ParentWithClassReferences>>();
                auto derived = gluecodium::python::dynamic_pointer_cast<ChildWithParentClassReferences>(base);
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
        .def(py::init([](std::shared_ptr<ChildWithParentClassReferences> native) {
            auto self = std::make_shared<ChildWithParentClassReferencesTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("class_function", [](ChildWithParentClassReferences& self) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.class_function(); });
        })
        .def_property("class_property", [](const ChildWithParentClassReferences& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_class_property();
            });
        }, [](ChildWithParentClassReferences& self, const ::std::shared_ptr< ::smoke::ParentClass >& value) {
            gluecodium::python::call_native([&] {
                self.set_class_property(value);
            });
        })
        ;


}
