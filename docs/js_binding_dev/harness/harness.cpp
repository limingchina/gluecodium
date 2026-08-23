#include <emscripten/bind.h>

#include "phase4/Harness.h"
#include "phase5/MultiClass.h"
#include "phase5/MultipleInheritanceFactory.h"
#include "phase5/JsCallback.h"

namespace phase4 {

namespace {

class HarnessImpl final : public Harness {
public:
    explicit HarnessImpl(const int32_t seed) : value(seed) {}

    int32_t increment(const int32_t amount) override {
        value += amount;
        return value;
    }

    std::optional<int32_t> nullable_value(const std::optional<int32_t>& input) override {
        return input;
    }

    int32_t sum(const std::vector<int32_t>& values) override {
        int32_t result = 0;
        for (const auto item : values) {
            result += item;
        }
        return result;
    }

    std::optional<int32_t> lookup(
        const std::unordered_map<std::string, int32_t>& values,
        const std::string& key
    ) override {
        const auto found = values.find(key);
        return found == values.end() ? std::nullopt : std::optional<int32_t>(found->second);
    }

    Sample round_trip(const Sample& sample) override {
        return sample;
    }

    Mode round_trip_mode(const Mode mode) override {
        return mode;
    }

    int64_t round_trip_long(const int64_t input) override {
        return input;
    }

    int32_t get_value() const override {
        return value;
    }

    void set_value(const int32_t newValue) override {
        value = newValue;
    }

private:
    int32_t value;
};

}  // namespace

std::shared_ptr<Harness> Harness::create(const int32_t seed) {
    return std::make_shared<HarnessImpl>(seed);
}

int32_t Harness::add(const int32_t first, const int32_t second) {
    return first + second;
}

}  // namespace phase4

namespace phase5 {

namespace {

class MultiClassImpl final : public MultiClass {
public:
    std::string parent_function() override { return "open-parent"; }
    std::string get_parent_property() const override { return "open-parent"; }
    void set_parent_property(const std::string&) override {}
    std::string parent_function_light() override { return "narrow-parent"; }
    std::string get_parent_property_light() const override { return "narrow-property"; }
    void set_parent_property_light(const std::string&) override {}
    std::string child_function() override { return "child"; }
    std::string get_child_property() const override { return "child-property"; }
    void set_child_property(const std::string&) override {}
};

}  // namespace

std::shared_ptr<MultiClass> MultipleInheritanceFactory::get_multi_class() {
    return std::make_shared<MultiClassImpl>();
}

std::shared_ptr<NarrowInterface> MultipleInheritanceFactory::get_multi_class_as_narrow() {
    return std::make_shared<MultiClassImpl>();
}

std::shared_ptr<NarrowInterface> MultipleInheritanceFactory::upcast_to_narrow(
    const std::shared_ptr<MultiClass>& instance
) {
    return instance;
}

std::string MultipleInheritanceFactory::invoke_js_callback(
    const std::shared_ptr<JsCallback>& callback
) {
    return callback->invoke("native");
}

std::string MultipleInheritanceFactory::invoke_lambda(
    const StringTransformer& callback,
    const std::string& value
) {
    return callback(value);
}

::Return<std::string, std::error_code> MultipleInheritanceFactory::invoke_throwing(
    const bool success
) {
    if (success) {
        return std::string("success");
    }
    return std::error_code(7, std::generic_category());
}

::std::error_code MultipleInheritanceFactory::invoke_throwing_void(
    const bool success
) {
    if (success) {
        return {};
    }
    return std::error_code(7, std::generic_category());
}

::Return<std::string, CallbackPayload> MultipleInheritanceFactory::invoke_payload_throwing(
    const bool success
) {
    if (success) {
        return std::string("payload-success");
    }
    return CallbackPayload{9, "payload failure"};
}

}  // namespace phase5
