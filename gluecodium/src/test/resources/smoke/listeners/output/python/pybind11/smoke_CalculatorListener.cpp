

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/CalculationResult.h"
#include "smoke/CalculatorListener.h"
#include "memory"
#include "string"
#include "unordered_map"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using CalculatorListener = ::smoke::CalculatorListener;

class CalculatorListenerTrampoline : public CalculatorListener {
public:
    using CalculatorListener::CalculatorListener;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<CalculatorListener> m_impl;

    void on_calculation_result(
            double calculation_result ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->on_calculation_result(calculation_result);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, CalculatorListener, on_calculation_result, calculation_result);
    }
    void on_calculation_result_const(
            double calculation_result ) const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->on_calculation_result_const(calculation_result);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, CalculatorListener, on_calculation_result_const, calculation_result);
    }
    void on_calculation_result_struct(
            const ::smoke::CalculatorListener::ResultStruct& calculation_result ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->on_calculation_result_struct(calculation_result);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, CalculatorListener, on_calculation_result_struct, calculation_result);
    }
    void on_calculation_result_array(
            const ::std::vector< double >& calculation_result ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->on_calculation_result_array(calculation_result);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, CalculatorListener, on_calculation_result_array, calculation_result);
    }
    void on_calculation_result_map(
            const ::std::unordered_map< ::std::string, double >& calculation_results ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->on_calculation_result_map(calculation_results);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, CalculatorListener, on_calculation_result_map, calculation_results);
    }
    void on_calculation_result_instance(
            const ::std::shared_ptr< ::smoke::CalculationResult >& calculation_result ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->on_calculation_result_instance(calculation_result);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, CalculatorListener, on_calculation_result_instance, calculation_result);
    }
};

void register_smoke_CalculatorListener(py::module_& module) {
    py::class_<CalculatorListener, std::shared_ptr<CalculatorListener>, CalculatorListenerTrampoline>(module, "CalculatorListener")
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<CalculatorListener> native) {
            auto self = std::make_shared<CalculatorListenerTrampoline>();
            self->m_impl = native;
            return self;
        }))
        ;
}

