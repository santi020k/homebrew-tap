# typed: strict
# frozen_string_literal: true

cask "coolstead" do
  version "1.0.0"
  sha256 "57fa8f392bd98ccbfdf9f865f672411542032e7963e6d0079c5b1701cfa8fff2"

  url "https://github.com/santi020k/coolstead-releases/releases/download/v#{version}/Coolstead-#{version}.dmg"
  name "Coolstead"
  desc "Thermal monitor and conservative fan controller"
  homepage "https://coolstead.santi020k.com/"

  depends_on macos: :sonoma

  app "Coolstead.app"

  uninstall quit: "com.santi020k.coolstead"

  caveats <<~EOS
    Monitoring works immediately. Fan control is optional and requires administrator
    approval in System Settings > General > Login Items & Extensions.

    Before uninstalling Coolstead, disable cooling and quit the app so every fan
    returns to macOS automatic control.
  EOS
end
