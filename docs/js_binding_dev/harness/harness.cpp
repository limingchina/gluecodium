#include <emscripten/bind.h>

#include "phase4/Harness.h"

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
