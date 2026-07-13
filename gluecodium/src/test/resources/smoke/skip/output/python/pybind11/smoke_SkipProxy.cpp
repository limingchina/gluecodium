

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SkipProxy.h"
#include "smoke/SkippedEverywhere.h"
#include "smoke/SkippedEverywhereEnum.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SkipProxy = ::gluecodium::smoke::SkipProxy;

class SkipProxyTrampoline : public SkipProxy {
public:
    using SkipProxy::SkipProxy;

    ::std::string not_in_java(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::string, SkipProxy, not_in_java, input);
    }
    bool not_in_swift(
            bool input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(bool, SkipProxy, not_in_swift, input);
    }
    float not_in_dart(
            float input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(float, SkipProxy, not_in_dart, input);
    }
    float not_in_kotlin(
            float input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(float, SkipProxy, not_in_kotlin, input);
    }
    ::std::string& get_skipped_in_java() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::string&, SkipProxy, get_skipped_in_java);
    }
    void set_skipped_in_java(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, SkipProxy, set_skipped_in_java, value);
    }
    bool is_skipped_in_swift() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(bool, SkipProxy, is_skipped_in_swift);
    }
    void set_skipped_in_swift(const bool value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, SkipProxy, set_skipped_in_swift, value);
    }
    float get_skipped_in_dart() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(float, SkipProxy, get_skipped_in_dart);
    }
    void set_skipped_in_dart(const float value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, SkipProxy, set_skipped_in_dart, value);
    }
    float get_skipped_in_kotlin() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(float, SkipProxy, get_skipped_in_kotlin);
    }
    void set_skipped_in_kotlin(const float value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, SkipProxy, set_skipped_in_kotlin, value);
    }
    ::smoke::SkippedEverywhere& get_skipped_everywhere() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::smoke::SkippedEverywhere&, SkipProxy, get_skipped_everywhere);
    }
    void set_skipped_everywhere(const ::smoke::SkippedEverywhere& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, SkipProxy, set_skipped_everywhere, value);
    }
    ::smoke::SkippedEverywhereEnum get_skipped_everywhere_too() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::smoke::SkippedEverywhereEnum, SkipProxy, get_skipped_everywhere_too);
    }
    void set_skipped_everywhere_too(const ::smoke::SkippedEverywhereEnum value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, SkipProxy, set_skipped_everywhere_too, value);
    }
};

void register_SkipProxy(py::module_& module) {
    py::class_<SkipProxy, std::shared_ptr<SkipProxy>, SkipProxyTrampoline>(module, "SkipProxy")
        .def(py::init<>())
        .def("not_in_java", &SkipProxy::not_in_java, py::arg("input"))
        .def("not_in_swift", &SkipProxy::not_in_swift, py::arg("input"))
        .def("not_in_dart", &SkipProxy::not_in_dart, py::arg("input"))
        .def("not_in_kotlin", &SkipProxy::not_in_kotlin, py::arg("input"))
        .def_property("skipped_in_java", py::overload_cast<>(&SkipProxy::get_skipped_in_java, py::const_), py::overload_cast<const ::std::string&>(&SkipProxy::set_skipped_in_java))
        .def_property("is_skipped_in_swift", py::overload_cast<>(&SkipProxy::is_skipped_in_swift, py::const_), py::overload_cast<const bool>(&SkipProxy::set_skipped_in_swift))
        .def_property("skipped_in_dart", py::overload_cast<>(&SkipProxy::get_skipped_in_dart, py::const_), py::overload_cast<const float>(&SkipProxy::set_skipped_in_dart))
        .def_property("skipped_in_kotlin", py::overload_cast<>(&SkipProxy::get_skipped_in_kotlin, py::const_), py::overload_cast<const float>(&SkipProxy::set_skipped_in_kotlin))
        .def_property("skipped_everywhere", py::overload_cast<>(&SkipProxy::get_skipped_everywhere, py::const_), py::overload_cast<const ::smoke::SkippedEverywhere&>(&SkipProxy::set_skipped_everywhere))
        .def_property("skipped_everywhere_too", py::overload_cast<>(&SkipProxy::get_skipped_everywhere_too, py::const_), py::overload_cast<const ::smoke::SkippedEverywhereEnum>(&SkipProxy::set_skipped_everywhere_too))
        ;
}

