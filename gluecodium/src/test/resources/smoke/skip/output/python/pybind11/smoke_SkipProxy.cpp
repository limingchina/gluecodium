

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SkipProxy.h"
#include "smoke/SkippedEverywhere.h"
#include "smoke/SkippedEverywhereEnum.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SkipProxy = ::smoke::SkipProxy;

class SkipProxyTrampoline : public SkipProxy {
public:
    using SkipProxy::SkipProxy;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<SkipProxy> m_impl;

    ::std::string not_in_java(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->not_in_java(input);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, SkipProxy, not_in_java, input);
    }
    bool not_in_swift(
            bool input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->not_in_swift(input);
        }
        PYBIND11_OVERRIDE_PURE(bool, SkipProxy, not_in_swift, input);
    }
    float not_in_dart(
            float input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->not_in_dart(input);
        }
        PYBIND11_OVERRIDE_PURE(float, SkipProxy, not_in_dart, input);
    }
    float not_in_kotlin(
            float input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->not_in_kotlin(input);
        }
        PYBIND11_OVERRIDE_PURE(float, SkipProxy, not_in_kotlin, input);
    }
    ::std::string get_skipped_in_java() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_skipped_in_java();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, SkipProxy, get_skipped_in_java);
    }
    void set_skipped_in_java(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_skipped_in_java(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, SkipProxy, set_skipped_in_java, value);
    }
    bool is_skipped_in_swift() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->is_skipped_in_swift();
        }
        PYBIND11_OVERRIDE_PURE(bool, SkipProxy, is_skipped_in_swift);
    }
    void set_skipped_in_swift(const bool value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_skipped_in_swift(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, SkipProxy, set_skipped_in_swift, value);
    }
    float get_skipped_in_dart() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_skipped_in_dart();
        }
        PYBIND11_OVERRIDE_PURE(float, SkipProxy, get_skipped_in_dart);
    }
    void set_skipped_in_dart(const float value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_skipped_in_dart(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, SkipProxy, set_skipped_in_dart, value);
    }
    float get_skipped_in_kotlin() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_skipped_in_kotlin();
        }
        PYBIND11_OVERRIDE_PURE(float, SkipProxy, get_skipped_in_kotlin);
    }
    void set_skipped_in_kotlin(const float value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_skipped_in_kotlin(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, SkipProxy, set_skipped_in_kotlin, value);
    }
    ::smoke::SkippedEverywhere get_skipped_everywhere() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_skipped_everywhere();
        }
        PYBIND11_OVERRIDE_PURE(::smoke::SkippedEverywhere, SkipProxy, get_skipped_everywhere);
    }
    void set_skipped_everywhere(const ::smoke::SkippedEverywhere& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_skipped_everywhere(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, SkipProxy, set_skipped_everywhere, value);
    }
    ::smoke::SkippedEverywhereEnum get_skipped_everywhere_too() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_skipped_everywhere_too();
        }
        PYBIND11_OVERRIDE_PURE(::smoke::SkippedEverywhereEnum, SkipProxy, get_skipped_everywhere_too);
    }
    void set_skipped_everywhere_too(const ::smoke::SkippedEverywhereEnum value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_skipped_everywhere_too(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, SkipProxy, set_skipped_everywhere_too, value);
    }
};

void register_smoke_SkipProxy(py::module_& module) {
    py::class_<SkipProxy, std::shared_ptr<SkipProxy>, SkipProxyTrampoline>(module, "SkipProxy")
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<SkipProxy> native) {
            auto self = std::make_shared<SkipProxyTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def_property("skipped_in_java", [](const SkipProxy& self) {
            return self.get_skipped_in_java();
        }, [](SkipProxy& self, const ::std::string& value) {
            self.set_skipped_in_java(value);
        })
        .def_property("is_skipped_in_swift", [](const SkipProxy& self) {
            return self.is_skipped_in_swift();
        }, [](SkipProxy& self, const bool value) {
            self.set_skipped_in_swift(value);
        })
        .def_property("skipped_in_dart", [](const SkipProxy& self) {
            return self.get_skipped_in_dart();
        }, [](SkipProxy& self, const float value) {
            self.set_skipped_in_dart(value);
        })
        .def_property("skipped_in_kotlin", [](const SkipProxy& self) {
            return self.get_skipped_in_kotlin();
        }, [](SkipProxy& self, const float value) {
            self.set_skipped_in_kotlin(value);
        })
        .def_property("skipped_everywhere", [](const SkipProxy& self) {
            return self.get_skipped_everywhere();
        }, [](SkipProxy& self, const ::smoke::SkippedEverywhere& value) {
            self.set_skipped_everywhere(value);
        })
        .def_property("skipped_everywhere_too", [](const SkipProxy& self) {
            return self.get_skipped_everywhere_too();
        }, [](SkipProxy& self, const ::smoke::SkippedEverywhereEnum value) {
            self.set_skipped_everywhere_too(value);
        })
        ;
}

