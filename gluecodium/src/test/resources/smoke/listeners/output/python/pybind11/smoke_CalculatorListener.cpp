

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/VectorHash.h"
#include "smoke/CalculationResult.h"
#include "smoke/CalculatorListener.h"
#include "memory"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using CalculatorListener = ::gluecodium::smoke::CalculatorListener;

class CalculatorListenerTrampoline : public CalculatorListener {
public:
    using CalculatorListener::CalculatorListener;

    void on_calculation_result(
            double calculation_result ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, CalculatorListener, on_calculation_result, calculation_result);
    }
    void on_calculation_result_const(
            double calculation_result ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, CalculatorListener, on_calculation_result_const, calculation_result);
    }
    void on_calculation_result_struct(
            const ::smoke::CalculatorListener::ResultStruct& calculation_result ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, CalculatorListener, on_calculation_result_struct, calculation_result);
    }
    void on_calculation_result_array(
            const ::std::vector< double >& calculation_result ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, CalculatorListener, on_calculation_result_array, calculation_result);
    }
    void on_calculation_result_map(
            const ::std::unordered_map< ::std::string, double >& calculation_results ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, CalculatorListener, on_calculation_result_map, calculation_results);
    }
    void on_calculation_result_instance(
            const ::std::shared_ptr< ::smoke::CalculationResult >& calculation_result ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, CalculatorListener, on_calculation_result_instance, calculation_result);
    }
};

void register_CalculatorListener(py::module_& module) {
    py::class_<CalculatorListener, std::shared_ptr<CalculatorListener>, CalculatorListenerTrampoline>(module, "CalculatorListener")
        .def("on_calculation_result", &CalculatorListener::on_calculation_result, py::arg("calculation_result"))
        .def("on_calculation_result_const", &CalculatorListener::on_calculation_result_const, py::arg("calculation_result"))
        .def("on_calculation_result_struct", &CalculatorListener::on_calculation_result_struct, py::arg("calculation_result"))
        .def("on_calculation_result_array", &CalculatorListener::on_calculation_result_array, py::arg("calculation_result"))
        .def("on_calculation_result_map", &CalculatorListener::on_calculation_result_map, py::arg("calculation_results"))
        .def("on_calculation_result_instance", &CalculatorListener::on_calculation_result_instance, py::arg("calculation_result"))
        ;
}

