// learning rust with this lol

use std::fs;
use std::error::Error;

// gotta do all this manually tragic

fn get_custom_mii() -> Result<rkg_utils::Mii, Box<dyn Error>> {

    let girl = true;

    let birthday = rkg_utils::header::mii::Birthday::new(6, 7)?;

    let color = rkg_utils::header::mii::FavoriteColor::Brown;

    let is_favorite = true;

    let name = String::from("tungtungtungsahur");

    let build = rkg_utils::header::mii::Build::new(67, 67)?;

    let mii_type = rkg_utils::header::mii::MiiType::Normal;
    
    let nd = chrono::NaiveDate::from_ymd_opt(2020, 6, 7).unwrap();
    let nt = chrono::NaiveTime::from_hms_opt(6, 7, 0).unwrap();
    let creation_date = chrono::NaiveDateTime::new(nd, nt);

    let system_id = 69;

    let shape = rkg_utils::header::mii::HeadShape::Flat; 
    let skin = rkg_utils::header::mii::SkinTone::Ivory;
    let face = rkg_utils::header::mii::FaceFeatures::Freckles;
    let head = rkg_utils::header::mii::Head::new(shape, skin, face);

    let mingle = false;

    let downloaded = false;

    let hair_type = rkg_utils::header::mii::HairType::PartingFrontTwoLongBackPonyTails;
    let hair_color = rkg_utils::header::mii::HairColor::Grizzly;
    let flip = false;
    let hair = rkg_utils::header::mii::Hair::new(hair_type, hair_color, flip);

    let eyebrow_type = rkg_utils::header::mii::EyebrowType::SoftAngledLarge;
    let eyebrows = rkg_utils::header::mii::Eyebrows::new(3, 2, 6, 7, hair_color, eyebrow_type)?;

    let eye_color = rkg_utils::header::mii::EyeColor::Green;
    let eye_type = rkg_utils::header::mii::EyeType::NormalLash;
    let eyes = rkg_utils::header::mii::Eyes::new(2, 5, 3, 9, eye_color, eye_type)?;

    let nose_type = rkg_utils::header::mii::NoseType::Rounded;
    let nose = rkg_utils::header::mii::Nose::new(2, 2, nose_type)?;

    let lips_type = rkg_utils::header::mii::LipsType::Malicious; // wtf does this even mean lmao
    let lips_color = rkg_utils::header::mii::LipsColor::Red;
    let lips = rkg_utils::header::mii::Lips::new(0, 3, lips_type, lips_color)?;

    let glasses_type = rkg_utils::header::mii::GlassesType::None;
    let glasses_color = rkg_utils::header::mii::GlassesColor::Black;
    let glasses = rkg_utils::header::mii::Glasses::new(0, 0, glasses_type, glasses_color)?;

    let beard_type = rkg_utils::header::mii::BeardType::None;
    let mustache_type = rkg_utils::header::mii::MustacheType::None;
    let facial_hair = rkg_utils::header::mii::FacialHair::new(beard_type, mustache_type, hair_color, 0, 0)?;

    let mole = rkg_utils::header::mii::Mole::new(false, 0, 0, 0)?;

    let creator_name = String::from("triple t");

    let mii = rkg_utils::Mii::new(girl, birthday, color, is_favorite, name, build, mii_type, creation_date, system_id, head, mingle, downloaded, hair, eyebrows, eyes, nose, lips, glasses, facial_hair, mole, creator_name);

    return Ok(mii);
}

fn main() -> Result<(), Box<dyn Error>> {

    let ghost_string = fs::read_to_string("../../files/testbc.txt")?;

    // constructing the header

    let ms_in_ghost = (ghost_string.len() as f64 * 500.0 * (1.0/60.0) + 1.0) as u32;
    let igt = rkg_utils::header::InGameTime::from_milliseconds(ms_in_ghost)?;

    let slot_id = rkg_utils::header::SlotId::BowsersCastle;

    let vehicle = rkg_utils::header::combo::Vehicle::Jetsetter;
    let character = rkg_utils::header::combo::Character::Waluigi;
    let combo = rkg_utils::Combo::new(vehicle, character)?;

    let date = rkg_utils::header::Date::new(2067, 6, 7)?;

    let controller = rkg_utils::header::Controller::WiiWheel;

    let transmission_mod = rkg_utils::header::TransmissionMod::Vanilla;

    let ghost_type = rkg_utils::header::GhostType::PlayerBest;

    let auto = true;

    let laps = 3;

    let lap_splits = [rkg_utils::header::InGameTime::from_milliseconds(ms_in_ghost)?; 11];

    let country = rkg_utils::header::location::constants::Country::Japan;
    let subregion = rkg_utils::header::location::constants::JapanSubregion::Tokyo;
    let version = rkg_utils::header::location::constants::Version::Vanilla;
    let location = rkg_utils::header::Location::find_exact(country.into(), subregion.into(), version).unwrap();

    let mii = rkg_utils::Mii::default();//get_custom_mii()?;

    let header = rkg_utils::Header::new(igt, slot_id, combo, date, controller, transmission_mod, ghost_type, auto, laps, lap_splits, location, mii);
    
    // constructing the input data

    let compressed = false;

    let mut controller_inputs = Vec::new();
    let mut even = false;
    let mut input_token = String::from("");

    for c in ghost_string.chars() {
        input_token.push(c);
        if even {
            let x: u8 = input_token.parse().unwrap();
            let drift_flag = rkg_utils::input_data::DriftFlag::Disabled;
            let dpad = rkg_utils::input_data::DPadButton::None;
            let stick = rkg_utils::input_data::StickInput::new(x, 7)?;
            let controller_input = rkg_utils::ControllerInput::new(true, false, false, drift_flag, false, false, false, dpad, stick, 1);
            controller_inputs.push(controller_input);
            input_token = String::from("");
        }
        even = !even;
    }

    let input_data = rkg_utils::InputData::new(controller_inputs, compressed)?;

    // creating the ghost object

    let mut ghost = rkg_utils::Ghost::new(header, input_data);

    let _ = ghost.save_to_file("../../files/testbc.rkg")?;

    Ok(())
}
