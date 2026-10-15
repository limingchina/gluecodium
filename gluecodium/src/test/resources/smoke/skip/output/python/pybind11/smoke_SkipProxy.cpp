

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
#include "smoke/SkipProxy.h"
#include "smoke/SkippedEverywhere.h"
#include "smoke/SkippedEverywhereEnum.h"
#include "string"

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
        if (m_impl) {
            return m_impl->not_in_java(input);
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const SkipProxy*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e6e6f74496e4a617661")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::string, SkipProxy, "__gluecodium_callback_736d6f6b652e536b697050726f78792e6e6f74496e4a617661", not_in_java, input);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, SkipProxy, not_in_java, input);
    }
    bool not_in_swift(
            const bool input ) override {
        if (m_impl) {
            return m_impl->not_in_swift(input);
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const SkipProxy*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e6e6f74496e5377696674")) {
        PYBIND11_OVERRIDE_PURE_NAME(bool, SkipProxy, "__gluecodium_callback_736d6f6b652e536b697050726f78792e6e6f74496e5377696674", not_in_swift, input);
        }
        PYBIND11_OVERRIDE_PURE(bool, SkipProxy, not_in_swift, input);
    }
    float not_in_dart(
            const float input ) override {
        if (m_impl) {
            return m_impl->not_in_dart(input);
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const SkipProxy*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e6e6f74496e44617274")) {
        PYBIND11_OVERRIDE_PURE_NAME(float, SkipProxy, "__gluecodium_callback_736d6f6b652e536b697050726f78792e6e6f74496e44617274", not_in_dart, input);
        }
        PYBIND11_OVERRIDE_PURE(float, SkipProxy, not_in_dart, input);
    }
    float not_in_kotlin(
            const float input ) override {
        if (m_impl) {
            return m_impl->not_in_kotlin(input);
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const SkipProxy*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e6e6f74496e4b6f746c696e")) {
        PYBIND11_OVERRIDE_PURE_NAME(float, SkipProxy, "__gluecodium_callback_736d6f6b652e536b697050726f78792e6e6f74496e4b6f746c696e", not_in_kotlin, input);
        }
        PYBIND11_OVERRIDE_PURE(float, SkipProxy, not_in_kotlin, input);
    }
    ::std::string get_skipped_in_java() const override {
        if (m_impl) {
            return m_impl->get_skipped_in_java();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const SkipProxy*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e4a617661_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::string, SkipProxy, "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e4a617661_get", get_skipped_in_java);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, SkipProxy, get_skipped_in_java);
    }
    void set_skipped_in_java(const ::std::string& value) override {
        if (m_impl) {
            m_impl->set_skipped_in_java(value);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const SkipProxy*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e4a617661_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, SkipProxy, "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e4a617661_set", set_skipped_in_java, value);
        }
        PYBIND11_OVERRIDE_PURE(void, SkipProxy, set_skipped_in_java, value);
    }
    bool is_skipped_in_swift() const override {
        if (m_impl) {
            return m_impl->is_skipped_in_swift();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const SkipProxy*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e5377696674_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(bool, SkipProxy, "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e5377696674_get", is_skipped_in_swift);
        }
        PYBIND11_OVERRIDE_PURE(bool, SkipProxy, is_skipped_in_swift);
    }
    void set_skipped_in_swift(const bool value) override {
        if (m_impl) {
            m_impl->set_skipped_in_swift(value);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const SkipProxy*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e5377696674_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, SkipProxy, "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e5377696674_set", set_skipped_in_swift, value);
        }
        PYBIND11_OVERRIDE_PURE(void, SkipProxy, set_skipped_in_swift, value);
    }
    float get_skipped_in_dart() const override {
        if (m_impl) {
            return m_impl->get_skipped_in_dart();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const SkipProxy*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e44617274_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(float, SkipProxy, "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e44617274_get", get_skipped_in_dart);
        }
        PYBIND11_OVERRIDE_PURE(float, SkipProxy, get_skipped_in_dart);
    }
    void set_skipped_in_dart(const float value) override {
        if (m_impl) {
            m_impl->set_skipped_in_dart(value);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const SkipProxy*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e44617274_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, SkipProxy, "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e44617274_set", set_skipped_in_dart, value);
        }
        PYBIND11_OVERRIDE_PURE(void, SkipProxy, set_skipped_in_dart, value);
    }
    float get_skipped_in_kotlin() const override {
        if (m_impl) {
            return m_impl->get_skipped_in_kotlin();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const SkipProxy*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e4b6f746c696e_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(float, SkipProxy, "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e4b6f746c696e_get", get_skipped_in_kotlin);
        }
        PYBIND11_OVERRIDE_PURE(float, SkipProxy, get_skipped_in_kotlin);
    }
    void set_skipped_in_kotlin(const float value) override {
        if (m_impl) {
            m_impl->set_skipped_in_kotlin(value);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const SkipProxy*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e4b6f746c696e_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, SkipProxy, "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e4b6f746c696e_set", set_skipped_in_kotlin, value);
        }
        PYBIND11_OVERRIDE_PURE(void, SkipProxy, set_skipped_in_kotlin, value);
    }
    ::smoke::SkippedEverywhere get_skipped_everywhere() const override {
        if (m_impl) {
            return m_impl->get_skipped_everywhere();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const SkipProxy*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b697070656445766572797768657265_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::smoke::SkippedEverywhere, SkipProxy, "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b697070656445766572797768657265_get", get_skipped_everywhere);
        }
        PYBIND11_OVERRIDE_PURE(::smoke::SkippedEverywhere, SkipProxy, get_skipped_everywhere);
    }
    void set_skipped_everywhere(const ::smoke::SkippedEverywhere& value) override {
        if (m_impl) {
            m_impl->set_skipped_everywhere(value);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const SkipProxy*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b697070656445766572797768657265_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, SkipProxy, "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b697070656445766572797768657265_set", set_skipped_everywhere, value);
        }
        PYBIND11_OVERRIDE_PURE(void, SkipProxy, set_skipped_everywhere, value);
    }
    ::smoke::SkippedEverywhereEnum get_skipped_everywhere_too() const override {
        if (m_impl) {
            return m_impl->get_skipped_everywhere_too();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const SkipProxy*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b697070656445766572797768657265546f6f_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::smoke::SkippedEverywhereEnum, SkipProxy, "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b697070656445766572797768657265546f6f_get", get_skipped_everywhere_too);
        }
        PYBIND11_OVERRIDE_PURE(::smoke::SkippedEverywhereEnum, SkipProxy, get_skipped_everywhere_too);
    }
    void set_skipped_everywhere_too(const ::smoke::SkippedEverywhereEnum value) override {
        if (m_impl) {
            m_impl->set_skipped_everywhere_too(value);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const SkipProxy*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b697070656445766572797768657265546f6f_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, SkipProxy, "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b697070656445766572797768657265546f6f_set", set_skipped_everywhere_too, value);
        }
        PYBIND11_OVERRIDE_PURE(void, SkipProxy, set_skipped_everywhere_too, value);
    }
};



void register_smoke_SkipProxy(py::module_& module) {
auto cls_SkipProxy = py::class_<SkipProxy, std::shared_ptr<SkipProxy>, SkipProxyTrampoline>(module, "smoke_SkipProxy")
        .def("__gluecodium_id__", [](const SkipProxy& self) {
            return gluecodium::python::native_identity(self);
        })
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
        .def("not_in_java", [](SkipProxy& self, const ::std::string& input) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.not_in_java(input); });
        }, py::arg("input"))
        .def("not_in_swift", [](SkipProxy& self, const bool input) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.not_in_swift(input); });
        }, py::arg("input"))
        .def("not_in_dart", [](SkipProxy& self, const float input) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.not_in_dart(input); });
        }, py::arg("input"))
        .def("not_in_kotlin", [](SkipProxy& self, const float input) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.not_in_kotlin(input); });
        }, py::arg("input"))
        .def_property("skipped_in_java", [](const SkipProxy& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_skipped_in_java();
            });
        }, [](SkipProxy& self, const ::std::string& value) {
            gluecodium::python::call_native([&] {
                self.set_skipped_in_java(value);
            });
        })
        .def_property("is_skipped_in_swift", [](const SkipProxy& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.is_skipped_in_swift();
            });
        }, [](SkipProxy& self, const bool value) {
            gluecodium::python::call_native([&] {
                self.set_skipped_in_swift(value);
            });
        })
        .def_property("skipped_in_dart", [](const SkipProxy& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_skipped_in_dart();
            });
        }, [](SkipProxy& self, const float value) {
            gluecodium::python::call_native([&] {
                self.set_skipped_in_dart(value);
            });
        })
        .def_property("skipped_in_kotlin", [](const SkipProxy& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_skipped_in_kotlin();
            });
        }, [](SkipProxy& self, const float value) {
            gluecodium::python::call_native([&] {
                self.set_skipped_in_kotlin(value);
            });
        })
        ;


}
