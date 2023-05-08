struct Bitstream {
    stream: Vec<u8>,
    buff: u8,
    buff_bits: u32,
    max_buff_bits: u32,
}

impl Bitstream {
    pub fn new() -> Self {
        Bitstream {
            stream: Vec::new(),
            buff: 0,
            buff_bits: 0,
            max_buff_bits: 8,
        }
    }

    pub fn write(&mut self, value: u32, bits: u32) -> Result<u32, &'static str> {

        if bits > 32 {
            return Err("invalid bits value");
        }

        for i in 0..bits {
            self.buff <<= 1;
            self.buff |= ((value >> (bits - i - 1)) & 1) as u8;
            self.buff_bits += 1;

            if self.buff_bits == self.max_buff_bits {
                self.stream.push(self.buff);
                self.buff = 0;
                self.buff_bits = 0;
            }
        }

        return Ok(bits);
    }

    pub fn end_writing(&mut self) {
        self.buff <<= self.max_buff_bits - self.buff_bits;
        self.stream.push(self.buff);
        self.buff = 0;
        self.buff_bits = 0;
    }

    pub fn read(&mut self, bits: u32) -> Result<u32, &'static str> {
        if bits == 0 || bits > 32 {
            return Err("invalid bits value");
        }

        let mut value: u32 = 0;

        for _ in 0..bits {
            if self.buff_bits == 0 {
                if self.stream.is_empty() {
                    return Err("stream is empty");
                }

                self.buff = self.stream.remove(0);
                self.buff_bits = self.max_buff_bits;
            }

            let bit: u32 = (self.buff >> self.max_buff_bits - 1) as u32;
            self.buff <<= 1;
            self.buff_bits -= 1;
            value <<= 1;
            value |= bit;
        }

        return Ok(value);
    }
}

fn check_for_zeros(samples: &Vec<u16>, start_index: usize, end_index: usize) -> bool{

    let samples_len: usize = samples.len();

    if start_index >= samples_len {
        return false;
    }

    let true_end_index: usize;

    if end_index > samples_len {
        true_end_index = samples_len;
    } else {
        true_end_index = end_index;
    }

    if start_index >= true_end_index {
        return false;
    }

    let is_all_zeros = samples.iter()
        .skip(start_index as usize)
        .take((true_end_index - start_index) as usize)
        .all(|&x| x == 0);

    return is_all_zeros;
}

use std::cmp::max;
use std::f64::consts::LN_2;

fn calculate_bits(data: &Vec<u16>, i: usize, samples_in_packet: usize) -> u32 {
    let max_value = (i..i + samples_in_packet).fold(0, |acc, x| max(acc, data[x] as u32));
    let bits = ((  as f64).ln() / LN_2 + 1.0).floor() as u32;
    bits
}

fn count_leading_zeros(samples: &Vec<u16>, start_index: usize) -> u32 {
    let mut counter = 0;
    for x in start_index..samples.len() {
        if samples[x] == 0 {
            counter += 1;
        } else {
            return counter;
        }
    }

    return counter;
}

pub fn bitpacking_encode(samples: &Vec<u16>, max_bitwidth: u32, save_bitwidth_bits: u32,
                         samples_in_packet: u32) -> Result<Vec<u8>, &'static str> {

    let rle_symbol: u32 = (1 << save_bitwidth_bits) - 1;
    let rle_bitwidth: u32 = 32;

    let mut stream: Bitstream = Bitstream::new();
    let mut samples_in_packet_counter = 0;
    let mut i = 0;
    let mut bits = 0;

    while i < samples.len() {
        if samples_in_packet_counter == 0 {
            if check_for_zeros(samples, i, i + samples_in_packet as usize) {
                bits = 0;
                let zero_counter = count_leading_zeros(samples, i);
                if zero_counter / samples_in_packet > 4 {
                    stream.write(rle_symbol, save_bitwidth_bits).unwrap();
                    stream.write(zero_counter, rle_bitwidth).unwrap();
                    i += zero_counter as usize;
                    continue;
                }
            } else {
                bits = calculate_bits(samples, i, samples_in_packet as usize);
            }

            if bits > max_bitwidth {
                return Err("invalid input data bitwidth")
            }

            if i + samples_in_packet as usize > samples.len() && bits == 0 {
                bits = 1
            }

            stream.write(bits, save_bitwidth_bits).unwrap();
        }

        stream.write(samples[i] as u32, bits).unwrap();
        i += 1;
        samples_in_packet_counter += 1;

        if samples_in_packet_counter == samples_in_packet {
            samples_in_packet_counter = 0;
        }
    }

    stream.end_writing();

    Ok(stream.stream)
}

pub fn bitpacking_decode(data: &Vec<u8>, target_size: u32, max_bitwidth: u32, save_bitwidth_bits: u32,
                         samples_in_packet: u16) -> Result<Vec<u16>, &'static str>{

    let rle_symbol: u32 = (1 << save_bitwidth_bits) - 1;
    let rle_bitwidth: u32 = 32;

    let mut out: Vec<u16> = Vec::new();
    let mut i = 0;
    let mut stream: Bitstream = Bitstream {stream: data.clone(), buff: 0, buff_bits: 0, max_buff_bits: 9};

    while i < target_size {
        let bits = stream.read(save_bitwidth_bits).unwrap();

        if bits == rle_symbol {
            let zero_counter = stream.read(rle_bitwidth).unwrap();
            for _ in 0..zero_counter {
                out.push(0);
            }
            i += zero_counter;
            continue;
        }

        if bits > max_bitwidth {
            return Err("invalid bits value, bigger than max bitwidth");
        }

        if bits > 0 {
            for _ in 0..samples_in_packet {
                out.push(stream.read(bits).unwrap() as u16);
            }
        } else {
            for _ in 0..samples_in_packet {
                out.push(0)
            }
        }

        i += samples_in_packet as u32;
    }

    Ok(out)
}

#[cfg(test)]
mod bitstream_tests {
    use super::*;

    #[test]
    fn test_write_and_read() {
        let mut bitstream: Bitstream = Bitstream::new();
        bitstream.write(5, 3).unwrap();
        bitstream.write(55, 22).unwrap();
        bitstream.write(56, 22).unwrap();
        bitstream.write(57, 22).unwrap();
        bitstream.write(58, 22).unwrap();
        bitstream.end_writing();


        let value = bitstream.read(3).unwrap();
        assert_eq!(5, value);

        let value2 = bitstream.read(22).unwrap();
        assert_eq!(55, value2);

        let value3 = bitstream.read(22).unwrap();
        assert_eq!(56, value3);

        let value4 = bitstream.read(22).unwrap();
        assert_eq!(57, value4);

        let value5 = bitstream.read(22).unwrap();
        assert_eq!(58, value5);
    }

    #[test]
    fn test_bitpacking() {
        let data: Vec<u16> = vec![1, 2, 3, 4, 5, 1, 2, 3, 4, 12];
        let stream = bitpacking_encode(&data, 16, 5, 3).unwrap();
        let decoded_data: Vec<u16> = bitpacking_decode(&stream, data.len() as u32, 16, 5, 3).unwrap();
        assert_eq!(data, decoded_data);
    }
}

fn main() {
    println!("hello, world!");
}
