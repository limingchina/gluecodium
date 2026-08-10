

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
        PYBIND11_OVERRIDE_PURE(::std::shared_ptr< ::smoke::IncludableClass >, ChildClassWithIncludes, root_method, input1, input2);
    }
    ::smoke::ShouldNotInclude not_in_java(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->not_in_java();
        }
        PYBIND11_OVERRIDE_PURE(::smoke::ShouldNotInclude, ChildClassWithIncludes, not_in_java);
    }
    ::std::function<void(const int64_t)> get_root_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_root_property();
        }
        PYBIND11_OVERRIDE_PURE(::std::function<void(const int64_t)>, ChildClassWithIncludes, get_root_property);
    }
    void set_root_property(const ::std::function<void(const int64_t)>& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_root_property(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ChildClassWithIncludes, set_root_property, value);
    }
    ::smoke::ShouldNotInclude get_not_in_java_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_not_in_java_property();
        }
        PYBIND11_OVERRIDE_PURE(::smoke::ShouldNotInclude, ChildClassWithIncludes, get_not_in_java_property);
    }
    void set_not_in_java_property(const ::smoke::ShouldNotInclude& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_not_in_java_property(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ChildClassWithIncludes, set_not_in_java_property, value);
    }
};



void register_smoke_ChildClassWithIncludes(py::module_& module) {
auto cls_ChildClassWithIncludes = py::class_<ChildClassWithIncludes, ::smoke::ParentInterfaceWithIncludes, std::shared_ptr<ChildClassWithIncludes>, ChildClassWithIncludesTrampoline>(module, "smoke_ChildClassWithIncludes")
        .def("__gluecodium_id__", [](const ChildClassWithIncludes& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
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
