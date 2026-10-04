

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
#include "smoke/ChildClassWithIncludes.h"
#include "smoke/IncludableClass.h"
#include "smoke/IncludableEnum.h"
#include "smoke/IncludableLambda.h"
#include "smoke/IncludableStruct.h"
#include "smoke/ParentInterfaceWithIncludes.h"
#include "smoke/ShouldNotInclude.h"
#include "cstdint"
#include "functional"
#include "memory"

using ChildClassWithIncludes = ::smoke::ChildClassWithIncludes;

class ChildClassWithIncludesTrampoline : public ChildClassWithIncludes {
public:
    using ChildClassWithIncludes::ChildClassWithIncludes;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<ChildClassWithIncludes> m_impl;

    ::std::shared_ptr< ::smoke::IncludableClass > root_method(
            const ::smoke::IncludableStruct& input1, const ::smoke::IncludableEnum input2 ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->root_method(input1, input2);
        }
        if (py::get_override(static_cast<const ChildClassWithIncludes*>(this), "__gluecodium_callback_736d6f6b652e506172656e74496e7465726661636557697468496e636c756465732e726f6f744d6574686f64")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::shared_ptr< ::smoke::IncludableClass >, ChildClassWithIncludes, "__gluecodium_callback_736d6f6b652e506172656e74496e7465726661636557697468496e636c756465732e726f6f744d6574686f64", root_method, input1, input2);
        }
        PYBIND11_OVERRIDE_PURE(::std::shared_ptr< ::smoke::IncludableClass >, ChildClassWithIncludes, root_method, input1, input2);
    }
    ::smoke::ShouldNotInclude not_in_java(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->not_in_java();
        }
        if (py::get_override(static_cast<const ChildClassWithIncludes*>(this), "__gluecodium_callback_736d6f6b652e506172656e74496e7465726661636557697468496e636c756465732e6e6f74496e4a617661")) {
        PYBIND11_OVERRIDE_PURE_NAME(::smoke::ShouldNotInclude, ChildClassWithIncludes, "__gluecodium_callback_736d6f6b652e506172656e74496e7465726661636557697468496e636c756465732e6e6f74496e4a617661", not_in_java);
        }
        PYBIND11_OVERRIDE_PURE(::smoke::ShouldNotInclude, ChildClassWithIncludes, not_in_java);
    }
    ::std::function<void(const int64_t)> get_root_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_root_property();
        }
        if (py::get_override(static_cast<const ChildClassWithIncludes*>(this), "__gluecodium_callback_736d6f6b652e506172656e74496e7465726661636557697468496e636c756465732e726f6f7450726f7065727479_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::function<void(const int64_t)>, ChildClassWithIncludes, "__gluecodium_callback_736d6f6b652e506172656e74496e7465726661636557697468496e636c756465732e726f6f7450726f7065727479_get", get_root_property);
        }
        PYBIND11_OVERRIDE_PURE(::std::function<void(const int64_t)>, ChildClassWithIncludes, get_root_property);
    }
    void set_root_property(const ::std::function<void(const int64_t)>& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_root_property(value);
            return;
        }
        if (py::get_override(static_cast<const ChildClassWithIncludes*>(this), "__gluecodium_callback_736d6f6b652e506172656e74496e7465726661636557697468496e636c756465732e726f6f7450726f7065727479_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, ChildClassWithIncludes, "__gluecodium_callback_736d6f6b652e506172656e74496e7465726661636557697468496e636c756465732e726f6f7450726f7065727479_set", set_root_property, value);
        }
        PYBIND11_OVERRIDE_PURE(void, ChildClassWithIncludes, set_root_property, value);
    }
    ::smoke::ShouldNotInclude get_not_in_java_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_not_in_java_property();
        }
        if (py::get_override(static_cast<const ChildClassWithIncludes*>(this), "__gluecodium_callback_736d6f6b652e506172656e74496e7465726661636557697468496e636c756465732e6e6f74496e4a61766150726f7065727479_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::smoke::ShouldNotInclude, ChildClassWithIncludes, "__gluecodium_callback_736d6f6b652e506172656e74496e7465726661636557697468496e636c756465732e6e6f74496e4a61766150726f7065727479_get", get_not_in_java_property);
        }
        PYBIND11_OVERRIDE_PURE(::smoke::ShouldNotInclude, ChildClassWithIncludes, get_not_in_java_property);
    }
    void set_not_in_java_property(const ::smoke::ShouldNotInclude& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_not_in_java_property(value);
            return;
        }
        if (py::get_override(static_cast<const ChildClassWithIncludes*>(this), "__gluecodium_callback_736d6f6b652e506172656e74496e7465726661636557697468496e636c756465732e6e6f74496e4a61766150726f7065727479_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, ChildClassWithIncludes, "__gluecodium_callback_736d6f6b652e506172656e74496e7465726661636557697468496e636c756465732e6e6f74496e4a61766150726f7065727479_set", set_not_in_java_property, value);
        }
        PYBIND11_OVERRIDE_PURE(void, ChildClassWithIncludes, set_not_in_java_property, value);
    }
};



void register_smoke_ChildClassWithIncludes(py::module_& module) {
auto cls_ChildClassWithIncludes = py::class_<ChildClassWithIncludes, ::smoke::ParentInterfaceWithIncludes, std::shared_ptr<ChildClassWithIncludes>, ChildClassWithIncludesTrampoline>(module, "smoke_ChildClassWithIncludes")
        .def("__gluecodium_id__", [](const ChildClassWithIncludes& self) {
            return gluecodium::python::native_identity(self);
        })
        .def_static("__gluecodium_downcast__", [](const py::object& native) -> py::object {
            try {
                auto base = native.cast<std::shared_ptr<::smoke::ParentInterfaceWithIncludes>>();
                auto derived = gluecodium::python::dynamic_pointer_cast<ChildClassWithIncludes>(base);
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
        .def(py::init([](std::shared_ptr<ChildClassWithIncludes> native) {
            auto self = std::make_shared<ChildClassWithIncludesTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("root_method", [](ChildClassWithIncludes& self, const ::smoke::IncludableStruct& input1, const ::smoke::IncludableEnum input2) {
            return self.root_method(input1, input2);
        }, py::arg("input1"), py::arg("input2"))
        .def("not_in_java", [](ChildClassWithIncludes& self) {
            return self.not_in_java();
        })
        .def_property("root_property", [](const ChildClassWithIncludes& self) {
            return self.get_root_property();
        }, [](ChildClassWithIncludes& self, const ::std::function<void(const int64_t)>& value) {
            self.set_root_property(value);
        })
        .def_property("not_in_java_property", [](const ChildClassWithIncludes& self) {
            return self.get_not_in_java_property();
        }, [](ChildClassWithIncludes& self, const ::smoke::ShouldNotInclude& value) {
            self.set_not_in_java_property(value);
        })
        ;


}
