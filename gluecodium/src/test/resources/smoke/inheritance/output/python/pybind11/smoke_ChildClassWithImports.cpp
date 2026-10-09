

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
#include "smoke/ChildClassWithImports.h"
#include "smoke/IncludableClass.h"
#include "smoke/IncludableEnum.h"
#include "smoke/IncludableLambda.h"
#include "smoke/IncludableStruct.h"
#include "smoke/ParentClassWithImports.h"
#include "cstdint"
#include "functional"
#include "memory"

using ChildClassWithImports = ::smoke::ChildClassWithImports;

class ChildClassWithImportsTrampoline : public ChildClassWithImports {
public:
    using ChildClassWithImports::ChildClassWithImports;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<ChildClassWithImports> m_impl;

    ::std::shared_ptr< ::smoke::IncludableClass > root_method(
            const ::smoke::IncludableStruct& input1, const ::smoke::IncludableEnum input2 ) override {
        if (m_impl) {
            return m_impl->root_method(input1, input2);
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ChildClassWithImports*>(this), "__gluecodium_callback_736d6f6b652e506172656e74436c61737357697468496d706f7274732e726f6f744d6574686f64")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::shared_ptr< ::smoke::IncludableClass >, ChildClassWithImports, "__gluecodium_callback_736d6f6b652e506172656e74436c61737357697468496d706f7274732e726f6f744d6574686f64", root_method, input1, input2);
        }
        PYBIND11_OVERRIDE_PURE(::std::shared_ptr< ::smoke::IncludableClass >, ChildClassWithImports, root_method, input1, input2);
    }
    ::std::function<void(const int64_t)> get_root_property() const override {
        if (m_impl) {
            return m_impl->get_root_property();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ChildClassWithImports*>(this), "__gluecodium_callback_736d6f6b652e506172656e74436c61737357697468496d706f7274732e726f6f7450726f7065727479_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::function<void(const int64_t)>, ChildClassWithImports, "__gluecodium_callback_736d6f6b652e506172656e74436c61737357697468496d706f7274732e726f6f7450726f7065727479_get", get_root_property);
        }
        PYBIND11_OVERRIDE_PURE(::std::function<void(const int64_t)>, ChildClassWithImports, get_root_property);
    }
    void set_root_property(const ::std::function<void(const int64_t)>& value) override {
        if (m_impl) {
            m_impl->set_root_property(value);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ChildClassWithImports*>(this), "__gluecodium_callback_736d6f6b652e506172656e74436c61737357697468496d706f7274732e726f6f7450726f7065727479_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, ChildClassWithImports, "__gluecodium_callback_736d6f6b652e506172656e74436c61737357697468496d706f7274732e726f6f7450726f7065727479_set", set_root_property, gluecodium::python::to_python_regular(value));
        }
        PYBIND11_OVERRIDE_PURE(void, ChildClassWithImports, set_root_property, gluecodium::python::to_python_regular(value));
    }
};



void register_smoke_ChildClassWithImports(py::module_& module) {
auto cls_ChildClassWithImports = py::class_<ChildClassWithImports, ::smoke::ParentClassWithImports, std::shared_ptr<ChildClassWithImports>, ChildClassWithImportsTrampoline>(module, "smoke_ChildClassWithImports")
        .def("__gluecodium_id__", [](const ChildClassWithImports& self) {
            return gluecodium::python::native_identity(self);
        })
        .def_static("__gluecodium_downcast__", [](const py::object& native) -> py::object {
            try {
                auto base = native.cast<std::shared_ptr<::smoke::ParentClassWithImports>>();
                auto derived = gluecodium::python::dynamic_pointer_cast<ChildClassWithImports>(base);
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
        .def(py::init([](std::shared_ptr<ChildClassWithImports> native) {
            auto self = std::make_shared<ChildClassWithImportsTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("root_method", &ChildClassWithImports::root_method, py::arg("input1"), py::arg("input2"), py::call_guard<py::gil_scoped_release>())
        .def_property("root_property", [](const ChildClassWithImports& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_root_property();
            }));
        }, [](ChildClassWithImports& self, const ::std::function<void(const int64_t)>& value) {
            gluecodium::python::call_native([&] {
                self.set_root_property(value);
            });
        })
        ;


}
