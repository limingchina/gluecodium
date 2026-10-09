

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
#include "smoke/IncludableClass.h"
#include "smoke/IncludableEnum.h"
#include "smoke/IncludableLambda.h"
#include "smoke/IncludableStruct.h"
#include "smoke/ParentClassWithImports.h"
#include "cstdint"
#include "functional"
#include "memory"

using ParentClassWithImports = ::smoke::ParentClassWithImports;

class ParentClassWithImportsTrampoline : public ParentClassWithImports {
public:
    using ParentClassWithImports::ParentClassWithImports;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<ParentClassWithImports> m_impl;

    ::std::shared_ptr< ::smoke::IncludableClass > root_method(
            const ::smoke::IncludableStruct& input1, const ::smoke::IncludableEnum input2 ) override {
        if (m_impl) {
            return m_impl->root_method(input1, input2);
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ParentClassWithImports*>(this), "__gluecodium_callback_736d6f6b652e506172656e74436c61737357697468496d706f7274732e726f6f744d6574686f64")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::shared_ptr< ::smoke::IncludableClass >, ParentClassWithImports, "__gluecodium_callback_736d6f6b652e506172656e74436c61737357697468496d706f7274732e726f6f744d6574686f64", root_method, input1, input2);
        }
        PYBIND11_OVERRIDE_PURE(::std::shared_ptr< ::smoke::IncludableClass >, ParentClassWithImports, root_method, input1, input2);
    }
    ::std::function<void(const int64_t)> get_root_property() const override {
        if (m_impl) {
            return m_impl->get_root_property();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ParentClassWithImports*>(this), "__gluecodium_callback_736d6f6b652e506172656e74436c61737357697468496d706f7274732e726f6f7450726f7065727479_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::function<void(const int64_t)>, ParentClassWithImports, "__gluecodium_callback_736d6f6b652e506172656e74436c61737357697468496d706f7274732e726f6f7450726f7065727479_get", get_root_property);
        }
        PYBIND11_OVERRIDE_PURE(::std::function<void(const int64_t)>, ParentClassWithImports, get_root_property);
    }
    void set_root_property(const ::std::function<void(const int64_t)>& value) override {
        if (m_impl) {
            m_impl->set_root_property(value);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ParentClassWithImports*>(this), "__gluecodium_callback_736d6f6b652e506172656e74436c61737357697468496d706f7274732e726f6f7450726f7065727479_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, ParentClassWithImports, "__gluecodium_callback_736d6f6b652e506172656e74436c61737357697468496d706f7274732e726f6f7450726f7065727479_set", set_root_property, gluecodium::python::to_python_regular(value));
        }
        PYBIND11_OVERRIDE_PURE(void, ParentClassWithImports, set_root_property, gluecodium::python::to_python_regular(value));
    }
};



void register_smoke_ParentClassWithImports(py::module_& module) {
auto cls_ParentClassWithImports = py::class_<ParentClassWithImports, std::shared_ptr<ParentClassWithImports>, ParentClassWithImportsTrampoline>(module, "smoke_ParentClassWithImports")
        .def("__gluecodium_id__", [](const ParentClassWithImports& self) {
            return gluecodium::python::native_identity(self);
        })
        // Adoption constructor: adopt an existing native instance returned by a factory into
        // the trampoline subclass and stash it in `m_impl` so virtual calls forward to the
        // real implementation instead of the pure-virtual stub. `init_alias` cannot be used
        // here because the returned instance is a foreign (non-trampoline) implementation;
        // instead we build a fresh trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<ParentClassWithImports> native) {
            auto self = std::make_shared<ParentClassWithImportsTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("root_method", &ParentClassWithImports::root_method, py::arg("input1"), py::arg("input2"), py::call_guard<py::gil_scoped_release>())
        .def_property("root_property", [](const ParentClassWithImports& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_root_property();
            }));
        }, [](ParentClassWithImports& self, const ::std::function<void(const int64_t)>& value) {
            gluecodium::python::call_native([&] {
                self.set_root_property(value);
            });
        })
        ;


}
